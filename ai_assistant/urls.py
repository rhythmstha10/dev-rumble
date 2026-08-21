from django.urls import path

from .views import ChatView, RecommendView, StudyPlanView

app_name = "ai_assistant"

urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
    path("recommend/", RecommendView.as_view(), name="recommend"),
    path("study-plan/", StudyPlanView.as_view(), name="study-plan"),
]
