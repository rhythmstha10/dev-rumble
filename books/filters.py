import django_filters
from .models import Book, Loan


class BookFilter(django_filters.FilterSet):
    """Filtering for simple books"""
    
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title'
    )
    
    author = django_filters.CharFilter(
        field_name='author',
        lookup_expr='icontains',
        label='Author'
    )
    
    available_only = django_filters.BooleanFilter(
        method='filter_available_only',
        label='Available Only'
    )
    
    ordering = django_filters.OrderingFilter(
        fields=(
            ('title', 'Title (A-Z)'),
            ('-title', 'Title (Z-A)'),
            ('-available_copies', 'Most Available'),
            ('available_copies', 'Least Available'),
        ),
    )

    class Meta:
        model = Book
        fields = []

    def filter_available_only(self, queryset, name, value):
        if value:
            return queryset.filter(available_copies__gt=0)
        return queryset


class SimpleLoanFilter(django_filters.FilterSet):
    """Filtering for simple loans"""
    
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
            ('-due_date', 'Due Soon'),
            ('due_date', 'Due Later'),
        ),
    )

    class Meta:
        model = Loan
        fields = []
