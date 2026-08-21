from django.conf import settings
from django.db import models


class ChatMessage(models.Model):
    """One turn of the Campus AI conversation, stored for history / debugging."""

    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_chat_messages",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    # Optional: which "intent" the backend router picked for a user message
    # (e.g. "my_books", "due_date", "recommend", "general"). Blank for
    # assistant messages / when routing wasn't needed.
    intent = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user} [{self.role}]: {self.content[:40]}"


class StudyPlanRequest(models.Model):
    """Record of a generated study plan, so a student can revisit past plans."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_study_plans",
    )
    subject = models.CharField(max_length=255)
    days_until_exam = models.PositiveSmallIntegerField()
    hours_per_day = models.DecimalField(max_digits=4, decimal_places=1, default=2)
    plan_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.subject} ({self.days_until_exam}d)"
