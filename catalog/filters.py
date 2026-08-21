import django_filters
from .models import Book, Author, Category


class BookFilter(django_filters.FilterSet):
    """Advanced filtering for books"""
    
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Book Title'
    )
    
    author = django_filters.ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Author'
    )
    
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Category'
    )
    
    isbn = django_filters.CharFilter(
        field_name='isbn',
        lookup_expr='icontains',
        label='ISBN'
    )
    
    published_date_from = django_filters.DateFilter(
        field_name='published_date',
        lookup_expr='gte',
        label='Published After'
    )
    
    published_date_to = django_filters.DateFilter(
        field_name='published_date',
        lookup_expr='lte',
        label='Published Before'
    )
    
    available_only = django_filters.BooleanFilter(
        method='filter_available_only',
        label='Only Available Books'
    )
    
    ordering = django_filters.OrderingFilter(
        fields=(
            ('title', 'Title (A-Z)'),
            ('-title', 'Title (Z-A)'),
            ('published_date', 'Oldest First'),
            ('-published_date', 'Newest First'),
            ('available_copies', 'Least Available'),
            ('-available_copies', 'Most Available'),
        ),
        label='Sort By'
    )

    class Meta:
        model = Book
        fields = []

    def filter_available_only(self, queryset, name, value):
        """Filter books with available copies"""
        if value:
            return queryset.filter(available_copies__gt=0)
        return queryset
