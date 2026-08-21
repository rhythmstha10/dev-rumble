"""
Campus AI chat orchestration.
"""
import re

from ai_assistant.models import ChatMessage
from ai_assistant.services import context_builder, gemini_client, study_plan_engine
from ai_assistant.services.recommend_engine import recommend_books


def _detect_intent(message: str) -> str:
    text = message.lower()
    if "due" in text or "when is" in text:
        return "due_date"
    if any(kw in text for kw in ["what book", "my book", "currently have", "which book"]):
        return "my_books"
    if "renew" in text:
        return "renew"
    if "fine" in text or "owe" in text:
        return "fines"
    if "study plan" in text or ("plan" in text and ("day" in text or "exam" in text)):
        return "study_plan"
    if "available" in text and ("book" in text or "about" in text or " on " in text):
        return "browse_catalog"
    if any(kw in text for kw in [
        "recommend", "suggest", "should i read", "what should i study",
        "exam", "prepare for",
    ]):
        return "recommend"
    return "general"


def _extract_subject(message: str) -> str | None:
    text = message.lower()
    for marker in ["for ", "about ", "on ", "in "]:
        if marker in text:
            after = text.split(marker, 1)[1].strip()
            after = after.rstrip("?.! ")
            if 2 < len(after) < 60 and after not in {"me", "now", "general", "a while"}:
                return after
    return None


def _extract_days(message: str, default: int = 7) -> int:
    match = re.search(r"(\d+)\s*day", message.lower())
    return int(match.group(1)) if match else default


def _extract_hours(message: str, default: float = 2.0) -> float:
    match = re.search(r"(\d+(?:\.\d+)?)\s*hour", message.lower())
    return float(match.group(1)) if match else default


def _match_loan_by_title(message: str, loans: list[dict]) -> dict | None:
    """If the message mentions a specific borrowed book's title, return just
    that loan instead of the full list - e.g. 'when is my DBMS book due'."""
    text = message.lower()
    for loan in loans:
        title_words = [w for w in loan["book_title"].lower().split() if len(w) > 3]
        if any(w in text for w in title_words):
            return loan
    return None


def _infer_follow_up_intent(message: str, context: dict) -> str | None:
    """Reuse the previous user intent for short, ambiguous follow-ups."""
    words = re.findall(r"[a-z0-9']+", message.lower())
    if len(words) > 10 or not context["recent_messages"]:
        return None
    previous_users = [
        item for item in context["recent_messages"]
        if item["role"] == "user" and item.get("intent")
    ]
    if not previous_users:
        return None
    if any(word in words for word in ("that", "those", "other", "it", "also", "more")):
        return previous_users[-1]["intent"]
    return None


def _fallback_answer(intent: str, message: str, context: dict) -> str:
    loans = context["current_loans"]

    if intent in ("my_books", "due_date"):
        if not loans:
            return "You don't currently have any books borrowed."
        matched = _match_loan_by_title(message, loans) if intent == "due_date" else None
        target = [matched] if matched else loans
        lines = []
        for loan in target:
            flag = " (OVERDUE)" if loan["status"] == "overdue" else ""
            lines.append(f"- {loan['book_title']} — due {loan['due_date']}{flag}")
        prefix = "" if matched else "Here's what you currently have:\n"
        return prefix + "\n".join(lines)

    if intent == "renew":
        if not loans:
            return "You don't have any active loans to renew."
        lines = []
        for loan in loans:
            if loan["renewals_left"] > 0:
                lines.append(f"- {loan['book_title']}: eligible ({loan['renewals_left']} renewal(s) left)")
            else:
                lines.append(f"- {loan['book_title']}: not eligible (renewal limit reached)")
        return "Renewal status:\n" + "\n".join(lines)

    if intent == "fines":
        fines = context["fines"]
        if fines["total_unpaid"] <= 0:
            return "You have no unpaid fines. Nice!"
        lines = [f"- {i['book_title']}: Rs. {i['amount']:.2f}" for i in fines["items"]]
        return f"You owe Rs. {fines['total_unpaid']:.2f} in total:\n" + "\n".join(lines)

    if intent == "browse_catalog":
        books = context["available_books"]
        if not books:
            return "I couldn't find any available books matching that topic right now."
        lines = [f"- {b['title']} by {b['author']} ({b['available_copies']} copies available)" for b in books]
        return "Here's what's available:\n" + "\n".join(lines)

    if intent == "recommend":
        subject = _extract_subject(message)
        recs = recommend_books(context, subject=subject)
        if not recs:
            return "I don't have enough borrowing history yet to personalize recommendations - try browsing the catalog!"
        header = f"Here are a few books for {subject}:" if subject else "Here are a few books you might like:"
        lines = [f"- {r['title']} by {r['author']}: {r['reason']}" for r in recs]
        return header + "\n" + "\n".join(lines)

    if loans:
        return (
            f"I can help with your library account. You currently have {len(loans)} book(s) "
            "borrowed. Try asking things like \"what books do I have\", \"when is my book due\", "
            "\"can I renew\", \"recommend me books for <subject>\", or \"make me a study plan for <subject>\"."
        )
    return (
        "I can help with your library account, due dates, renewals, fines, book "
        "recommendations, and study plans. Try asking me something like \"recommend books "
        "for Database Systems\" or \"make me a 7-day study plan for DBMS\"."
    )


def _build_prompt(message: str, context: dict) -> str:
    return (
        "You are Campus AI, a helpful assistant inside a university library platform. "
        "Answer the student's question concisely (2-5 sentences). For anything about "
        "their library account, borrowed books, due dates, fines, or recommendations, "
        "use ONLY the data given below - never invent book titles, dates, or amounts "
        "that aren't in the data. For general questions unrelated to the library "
        "(study help, general knowledge, etc.), answer normally and helpfully.\n\n"
        f"Student's current loans: {context['current_loans']}\n"
        f"Student's recent loan history: {context['loan_history']}\n"
        f"Student's fines: {context['fines']}\n"
        f"Sample of available catalog books: {context['available_books']}\n\n"
        f"Recent conversation: {context['recent_messages']}\n\n"
        f"Student's question: {message}"
    )


def handle_chat_message(user, message: str) -> dict:
    intent = _detect_intent(message)

    # Study plans have their own dedicated engine (with its own Gemini/fallback
    # logic already built in) - route straight there instead of the generic path.
    if intent == "study_plan":
        subject = _extract_subject(message) or "your upcoming exam"
        days = _extract_days(message)
        hours = _extract_hours(message)
        result = study_plan_engine.generate_study_plan(
            user, subject=subject, days=days, hours_per_day=hours
        )
        ChatMessage.objects.create(user=user, role="user", content=message, intent=intent)
        ChatMessage.objects.create(user=user, role="assistant", content=result["plan"], intent=intent)
        return {"reply": result["plan"], "intent": intent, "used_ai": result["used_ai"]}

    context = context_builder.build_chat_context(user)
    if intent == "general":
        intent = _infer_follow_up_intent(message, context) or intent

    if intent == "browse_catalog":
        subject = _extract_subject(message)
        if subject:
            context["available_books"] = context_builder.get_available_books(
                category_name=subject, limit=10
            )

    used_ai = False
    try:
        reply = gemini_client.generate(_build_prompt(message, context))
        used_ai = True
    except gemini_client.GeminiUnavailableError:
        reply = _fallback_answer(intent, message, context)

    ChatMessage.objects.create(user=user, role="user", content=message, intent=intent)
    ChatMessage.objects.create(user=user, role="assistant", content=reply, intent=intent)

    return {"reply": reply, "intent": intent, "used_ai": used_ai}