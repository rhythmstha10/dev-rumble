from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    ChatRequestSerializer,
    RecommendRequestSerializer,
    StudyPlanRequestSerializer,
)
from .services.chat_engine import handle_chat_message
from .services.recommend_engine import get_recommendations_for_user
from .services.study_plan_engine import generate_study_plan


class ChatView(APIView):
    """POST /api/ai/chat/  { "message": "what books do I have?" }

    Auth required (session). Only ever reads the authenticated user's own
    data - see ai_assistant/services/context_builder.py.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = handle_chat_message(request.user, serializer.validated_data["message"])
        return Response(result, status=status.HTTP_200_OK)


class RecommendView(APIView):
    """POST /api/ai/recommend/  { "subject": "Database Systems" }  (subject optional)"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RecommendRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = get_recommendations_for_user(
            request.user,
            subject=data.get("subject") or None,
            limit=data.get("limit", 5),
        )
        return Response(result, status=status.HTTP_200_OK)


class StudyPlanView(APIView):
    """POST /api/ai/study-plan/  { "subject": "DBMS", "days_until_exam": 7, "hours_per_day": 2 }"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StudyPlanRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = generate_study_plan(
            request.user,
            subject=data["subject"],
            days=data["days_until_exam"],
            hours_per_day=data["hours_per_day"],
        )
        return Response(result, status=status.HTTP_200_OK)
