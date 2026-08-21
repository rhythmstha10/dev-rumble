"""
Tests run with NO GEMINI_API_KEY set, so they exercise the fallback path -
this is deliberate: it's what proves the feature works before a key exists.
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from catalog.models import Author, Book, Category
from circulation_app.models import Fine, Loan
from ai_assistant.models import ChatMessage, StudyPlanRequest
from ai_assistant.services import chat_engine, context_builder, recommend_engine

User = get_user_model()


@override_settings(GEMINI_API_KEY="")
class ContextBuilderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pw12345")
        self.author = Author.objects.create(name="C.J. Date")
        self.category = Category.objects.create(name="Database Systems")
        self.book = Book.objects.create(
            title="Database System Concepts",
            isbn="1111111111111",
            author=self.author,
            category=self.category,
            published_date=timezone.now().date(),
            total_copies=3,
            available_copies=2,
        )
        self.loan = Loan.objects.create(
            user=self.user,
            book=self.book,
            due_date=timezone.now() + timedelta(days=5),
        )

    def test_current_loans_reflects_real_loan(self):
        loans = context_builder.get_current_loans(self.user)
        self.assertEqual(len(loans), 1)
        self.assertEqual(loans[0]["book_title"], "Database System Concepts")

    def test_overdue_detected_dynamically(self):
        self.loan.due_date = timezone.now() - timedelta(days=1)
        self.loan.save()
        loans = context_builder.get_current_loans(self.user)
        self.assertEqual(loans[0]["status"], "overdue")

    def test_fines_only_unpaid_and_only_this_user(self):
        other_user = User.objects.create_user(username="bob", password="pw12345")
        other_loan = Loan.objects.create(
            user=other_user, book=self.book, due_date=timezone.now() + timedelta(days=5)
        )
        Fine.objects.create(loan=self.loan, amount=50, is_paid=False)
        Fine.objects.create(loan=other_loan, amount=999, is_paid=False)

        fines = context_builder.get_fines(self.user)
        self.assertEqual(fines["total_unpaid"], 50.0)
        self.assertEqual(len(fines["items"]), 1)

    def test_available_books_filters_out_of_stock(self):
        Book.objects.create(
            title="Out Of Stock Book",
            isbn="2222222222222",
            author=self.author,
            category=self.category,
            published_date=timezone.now().date(),
            total_copies=1,
            available_copies=0,
        )
        titles = [b["title"] for b in context_builder.get_available_books()]
        self.assertIn("Database System Concepts", titles)
        self.assertNotIn("Out Of Stock Book", titles)

    def test_available_books_matches_subject_in_title(self):
        python_book = Book.objects.create(
            title="Python Data Analysis",
            isbn="4444444444444",
            author=self.author,
            category=Category.objects.create(name="Programming"),
            published_date=timezone.now().date(),
            total_copies=1,
            available_copies=1,
        )
        titles = [
            book["title"]
            for book in context_builder.get_available_books(category_name="Python")
        ]
        self.assertIn(python_book.title, titles)


@override_settings(GEMINI_API_KEY="")
class ChatEngineFallbackTests(TestCase):
    """No API key configured -> must use deterministic fallback, never crash."""

    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pw12345")
        author = Author.objects.create(name="C.J. Date")
        category = Category.objects.create(name="Database Systems")
        self.book = Book.objects.create(
            title="Database System Concepts",
            isbn="1111111111111",
            author=author,
            category=category,
            published_date=timezone.now().date(),
            total_copies=3,
            available_copies=2,
        )
        Loan.objects.create(
            user=self.user, book=self.book, due_date=timezone.now() + timedelta(days=5)
        )

    def test_my_books_intent_lists_real_book(self):
        result = chat_engine.handle_chat_message(self.user, "What books do I currently have?")
        self.assertFalse(result["used_ai"])
        self.assertIn("Database System Concepts", result["reply"])
        self.assertEqual(result["intent"], "my_books")

    def test_no_data_leak_between_users(self):
        other = User.objects.create_user(username="carol", password="pw12345")
        result = chat_engine.handle_chat_message(other, "What books do I currently have?")
        self.assertNotIn("Database System Concepts", result["reply"])

    def test_chat_messages_persisted(self):
        chat_engine.handle_chat_message(self.user, "When is my book due?")
        self.assertEqual(ChatMessage.objects.filter(user=self.user).count(), 2)

    def test_unknown_message_does_not_crash(self):
        result = chat_engine.handle_chat_message(self.user, "asdkjaslkdjalksjd")
        self.assertEqual(result["intent"], "general")
        self.assertTrue(len(result["reply"]) > 0)

    def test_short_follow_up_reuses_previous_intent(self):
        first = chat_engine.handle_chat_message(self.user, "When is my book due?")
        follow_up = chat_engine.handle_chat_message(self.user, "What about the other one?")
        self.assertEqual(first["intent"], "due_date")
        self.assertEqual(follow_up["intent"], "due_date")


@override_settings(GEMINI_API_KEY="")
class RecommendEngineTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pw12345")
        author = Author.objects.create(name="C.J. Date")
        self.category = Category.objects.create(name="Database Systems")
        self.borrowed_book = Book.objects.create(
            title="Database System Concepts",
            isbn="1111111111111",
            author=author,
            category=self.category,
            published_date=timezone.now().date(),
            total_copies=2,
            available_copies=1,
        )
        self.other_book = Book.objects.create(
            title="SQL Performance Explained",
            isbn="3333333333333",
            author=author,
            category=self.category,
            published_date=timezone.now().date(),
            total_copies=2,
            available_copies=2,
        )
        Loan.objects.create(
            user=self.user, book=self.borrowed_book, due_date=timezone.now() + timedelta(days=5)
        )

    def test_does_not_recommend_currently_borrowed_book(self):
        result = recommend_engine.get_recommendations_for_user(self.user)
        titles = [r["title"] for r in result["recommendations"]]
        self.assertNotIn("Database System Concepts", titles)

    def test_recommends_real_catalog_book_in_same_category(self):
        result = recommend_engine.get_recommendations_for_user(self.user)
        titles = [r["title"] for r in result["recommendations"]]
        self.assertIn("SQL Performance Explained", titles)


@override_settings(GEMINI_API_KEY="")
class StudyPlanEngineTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pw12345")

    def test_plan_has_a_line_per_day(self):
        from ai_assistant.services.study_plan_engine import generate_study_plan

        result = generate_study_plan(self.user, subject="DBMS", days=3, hours_per_day=2)
        for day in ["Day 1", "Day 2", "Day 3"]:
            self.assertIn(day, result["plan"])
        self.assertFalse(result["used_ai"])

    def test_plan_persisted(self):
        from ai_assistant.services.study_plan_engine import generate_study_plan

        generate_study_plan(self.user, subject="DBMS", days=3, hours_per_day=2)
        self.assertEqual(StudyPlanRequest.objects.filter(user=self.user).count(), 1)


@override_settings(GEMINI_API_KEY="")
class ApiEndpointTests(TestCase):
    """Hits the real DRF views + URLs, through session auth, like the real frontend will."""

    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pw12345")
        author = Author.objects.create(name="C.J. Date")
        category = Category.objects.create(name="Database Systems")
        self.book = Book.objects.create(
            title="Database System Concepts",
            isbn="1111111111111",
            author=author,
            category=category,
            published_date=timezone.now().date(),
            total_copies=2,
            available_copies=2,
        )
        self.client = APIClient()

    def test_chat_requires_authentication(self):
        response = self.client.post("/api/ai/chat/", {"message": "hi"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_chat_endpoint_returns_reply(self):
        self.client.login(username="alice", password="pw12345")
        response = self.client.post(
            "/api/ai/chat/", {"message": "what books do I have?"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("reply", response.data)

    def test_recommend_endpoint(self):
        self.client.login(username="alice", password="pw12345")
        response = self.client.post("/api/ai/recommend/", {}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("recommendations", response.data)

    def test_study_plan_endpoint(self):
        self.client.login(username="alice", password="pw12345")
        response = self.client.post(
            "/api/ai/study-plan/",
            {"subject": "DBMS", "days_until_exam": 5, "hours_per_day": 2},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Day 1", response.data["plan"])
