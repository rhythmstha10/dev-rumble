"""
Builds the small, controlled JSON-able context that gets handed to the AI.

This is the ONLY place the ai_assistant app is allowed to read from
catalog / circulation_app models directly. Nothing here writes to the
database, and nothing here is ever passed to the LLM except plain data
(book titles, dates, numbers) - never raw querysets or model instances.
"""
from decimal import Decimal

from django.utils import timezone
from django.db.models import Q

from catalog.models import Book
from circulation_app.models import Loan, Fine
from ai_assistant.models import ChatMessage


def _loan_to_dict(loan: Loan) -> dict:
    is_overdue = (
        loan.status in ("borrowed", "overdue")
        and loan.due_date is not None
        and loan.due_date < timezone.now()
    )
    return {
        "loan_id": loan.id,
        "book_title": loan.book.title,
        "book_id": loan.book_id,
        "author": loan.book.author.name,
        "category": loan.book.category.name,
        "borrow_date": loan.borrow_date.date().isoformat(),
        "due_date": loan.due_date.date().isoformat() if loan.due_date else None,
        "status": "overdue" if is_overdue else loan.status,
        "renewed_count": loan.renewed_count,
        "renewals_left": max(Loan.MAX_RENEWALS - loan.renewed_count, 0),
    }


def get_current_loans(user) -> list[dict]:
    """Active (not yet returned) loans for this user, most-recently-due first."""
    qs = (
        Loan.objects.filter(user=user, status__in=["borrowed", "overdue"])
        .select_related("book", "book__author", "book__category")
        .order_by("due_date")
    )
    return [_loan_to_dict(loan) for loan in qs]


def get_loan_history(user, limit: int = 10) -> list[dict]:
    """Past (returned) loans, most recent first - used for recommendations."""
    qs = (
        Loan.objects.filter(user=user, status="returned")
        .select_related("book", "book__author", "book__category")
        .order_by("-return_date")[:limit]
    )
    return [_loan_to_dict(loan) for loan in qs]


def get_fines(user) -> dict:
    unpaid = Fine.objects.filter(loan__user=user, is_paid=False).select_related("loan__book")
    total = sum((f.amount for f in unpaid), Decimal("0"))
    return {
        "total_unpaid": float(total),
        "items": [
            {
                "book_title": f.loan.book.title,
                "amount": float(f.amount),
                "loan_id": f.loan_id,
            }
            for f in unpaid
        ],
    }


def get_available_books(category_name: str | None = None, limit: int = 15) -> list[dict]:
    """A slice of the real catalog, optionally filtered by category name, for
    grounding recommendations in books that actually exist and are in stock."""
    qs = Book.objects.select_related("author", "category").filter(available_copies__gt=0)
    if category_name:
        qs = qs.filter(
            Q(category__name__icontains=category_name)
            | Q(title__icontains=category_name)
            | Q(author__name__icontains=category_name)
            | Q(description__icontains=category_name)
        )
    qs = qs.order_by("-available_copies")[:limit]
    return [
        {
            "book_id": b.id,
            "title": b.title,
            "author": b.author.name,
            "category": b.category.name,
            "available_copies": b.available_copies,
        }
        for b in qs
    ]


def get_recent_chat_messages(user, limit: int = 6) -> list[dict]:
    """Return a short, user-scoped conversation window for follow-up questions."""
    messages = ChatMessage.objects.filter(user=user).order_by("-created_at")[:limit]
    return [
        {"role": message.role, "content": message.content, "intent": message.intent}
        for message in reversed(messages)
    ]


def build_chat_context(user) -> dict:
    """The bundle of real, user-scoped data handed to the AI for chat +
    recommendations. Kept intentionally small - only what a Campus AI
    answer would plausibly need."""
    current_loans = get_current_loans(user)
    history = get_loan_history(user)

    # Bias catalog sample towards categories the student has actually
    # engaged with, so recommendations aren't a random slice of the library.
    interest_categories = list(
        dict.fromkeys(
            [loan["category"] for loan in (current_loans + history)]
        )
    )[:3]

    available_books: list[dict] = []
    seen_ids = set()
    if interest_categories:
        for cat in interest_categories:
            for b in get_available_books(category_name=cat, limit=8):
                if b["book_id"] not in seen_ids:
                    available_books.append(b)
                    seen_ids.add(b["book_id"])
    else:
        available_books = get_available_books(limit=15)

    return {
        "student_name": user.get_username(),
        "current_loans": current_loans,
        "loan_history": history,
        "fines": get_fines(user),
        "available_books": available_books[:15],
        "recent_messages": get_recent_chat_messages(user),
    }
