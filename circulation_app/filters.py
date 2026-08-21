import django_filters
from .models import Loan, Fine


class LoanFilter(django_filters.FilterSet):
    """Filtering for loans"""
    
    status = django_filters.ChoiceFilter(
        choices=Loan.STATUS_CHOICES,
        label='Status'
    )
    
    user__username = django_filters.CharFilter(
        field_name='user__username',
        lookup_expr='icontains',
        label='User'
    )
    
    book__title = django_filters.CharFilter(
        field_name='book__title',
        lookup_expr='icontains',
        label='Book Title'
    )
    
    borrow_date_from = django_filters.DateFilter(
        field_name='borrow_date',
        lookup_expr='gte',
        label='Borrowed From'
    )
    
    borrow_date_to = django_filters.DateFilter(
        field_name='borrow_date',
        lookup_expr='lte',
        label='Borrowed To'
    )
    
    due_date_from = django_filters.DateFilter(
        field_name='due_date',
        lookup_expr='gte',
        label='Due Date From'
    )
    
    due_date_to = django_filters.DateFilter(
        field_name='due_date',
        lookup_expr='lte',
        label='Due Date To'
    )
    
    overdue_only = django_filters.BooleanFilter(
        method='filter_overdue_only',
        label='Overdue Only'
    )
    
    ordering = django_filters.OrderingFilter(
        fields=(
            ('-borrow_date', 'Most Recent'),
            ('borrow_date', 'Oldest'),
            ('-due_date', 'Due Soon'),
            ('due_date', 'Due Later'),
        ),
    )

    class Meta:
        model = Loan
        fields = []

    def filter_overdue_only(self, queryset, name, value):
        """Filter only overdue loans"""
        if value:
            from django.utils import timezone
            return queryset.filter(status='overdue')
        return queryset


class FineFilter(django_filters.FilterSet):
    """Filtering for fines"""
    
    is_paid = django_filters.BooleanFilter(label='Paid')
    
    loan__user__username = django_filters.CharFilter(
        field_name='loan__user__username',
        lookup_expr='icontains',
        label='User'
    )
    
    amount_min = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='gte',
        label='Amount Min'
    )
    
    amount_max = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='lte',
        label='Amount Max'
    )
    
    created_from = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Created From'
    )
    
    created_to = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Created To'
    )
    
    ordering = django_filters.OrderingFilter(
        fields=(
            ('-created_at', 'Most Recent'),
            ('created_at', 'Oldest'),
            ('-amount', 'Highest Amount'),
            ('amount', 'Lowest Amount'),
        ),
    )

    class Meta:
        model = Fine
        fields = []
