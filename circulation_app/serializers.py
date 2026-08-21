from rest_framework import serializers
from .models import Loan, Fine


class FineSerializer(serializers.ModelSerializer):
    loan_user = serializers.CharField(source='loan.user.username', read_only=True)
    loan_book = serializers.CharField(source='loan.book.title', read_only=True)

    class Meta:
        model = Fine
        fields = ['id', 'loan', 'loan_user', 'loan_book', 'amount', 'is_paid', 'created_at']
        read_only_fields = ['id', 'created_at']


class LoanSerializer(serializers.ModelSerializer):
    # Nested read-only fine info, shown automatically if a fine exists
    fine = FineSerializer(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Loan
        fields = [
            'id', 'user', 'user_username', 'book', 'book_title', 'borrow_date', 'due_date',
            'return_date', 'status', 'renewed_count', 'fine',
        ]
        read_only_fields = ['id', 'borrow_date', 'return_date', 'status', 'renewed_count']


class BorrowRequestSerializer(serializers.Serializer):
    """Not tied to a model — just validates the input when a user wants to borrow a book."""
    book_id = serializers.IntegerField()


class ReturnRequestSerializer(serializers.Serializer):
    """Validates the input when a user returns a book."""
    loan_id = serializers.IntegerField()