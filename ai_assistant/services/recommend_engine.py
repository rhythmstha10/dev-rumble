"""
Book recommendations grounded in the real catalog + the student's real
borrowing history. Works with or without Gemini - the "why" explanation
gets a nicer sentence from the LLM when available, but the underlying
book picks are always computed the same deterministic way, so recommended
books always genuinely exist and are in stock.
"""
from ai_assistant.services import context_builder, gemini_client


def _pick_candidates(context: dict, subject: str | None, limit: int) -> list[dict]:
    borrowed_ids = {loan["book_id"] for loan in context["current_loans"] + context["loan_history"]}

    pool = context["available_books"]
    if subject:
        subject_matches = context_builder.get_available_books(category_name=subject, limit=limit * 3)
        if subject_matches:
            pool = subject_matches

    candidates = [b for b in pool if b["book_id"] not in borrowed_ids]
    return candidates[:limit]


def _reason_for(book: dict, context: dict, subject: str | None) -> str:
    if subject:
        return f"it matches the subject you asked about ({subject})"
    history_categories = {loan["category"] for loan in context["loan_history"] + context["current_loans"]}
    if book["category"] in history_categories:
        return f"you've recently borrowed other {book['category']} books"
    return "it's a popular, well-stocked title in our catalog"


def recommend_books(context: dict, subject: str | None = None, limit: int = 5) -> list[dict]:
    candidates = _pick_candidates(context, subject, limit)
    return [
        {
            "book_id": b["book_id"],
            "title": b["title"],
            "author": b["author"],
            "category": b["category"],
            "reason": _reason_for(b, context, subject),
        }
        for b in candidates
    ]


def get_recommendations_for_user(user, subject: str | None = None, limit: int = 5) -> dict:
    context = context_builder.build_chat_context(user)
    recs = recommend_books(context, subject=subject, limit=limit)

    used_ai = False
    summary = None
    if recs and gemini_client.is_configured():
        prompt = (
            "In 1-2 friendly sentences, introduce this list of book recommendations "
            f"for a student{f' studying {subject}' if subject else ''}. "
            "Do not invent any titles beyond what's given.\n\n"
            f"Recommendations: {recs}"
        )
        try:
            summary = gemini_client.generate(prompt)
            used_ai = True
        except gemini_client.GeminiUnavailableError:
            summary = None

    if not summary:
        summary = (
            f"Based on your borrowing history, here are some books you might like:"
            if recs
            else "I don't have enough data yet to personalize recommendations - try browsing the catalog!"
        )

    return {"summary": summary, "recommendations": recs, "used_ai": used_ai}
