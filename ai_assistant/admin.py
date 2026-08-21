from django.contrib import admin

from .models import ChatMessage, StudyPlanRequest


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "intent", "created_at")
    list_filter = ("role", "intent")
    search_fields = ("user__username", "content")


@admin.register(StudyPlanRequest)
class StudyPlanRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "days_until_exam", "hours_per_day", "created_at")
    search_fields = ("user__username", "subject")
