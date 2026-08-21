from decimal import Decimal

from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000, allow_blank=False)


class RecommendRequestSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255, required=False, allow_blank=True)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=10, default=5)


class StudyPlanRequestSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255, allow_blank=False)
    days_until_exam = serializers.IntegerField(min_value=1, max_value=30)
    hours_per_day = serializers.DecimalField(
        max_digits=4, decimal_places=1, min_value=Decimal("0.5"), max_value=Decimal("16")
    )
