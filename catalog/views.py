from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from accounts.permissions import IsLibrarianOrSuperAdmin
from .models import Author, Category, Book
from .serializers import AuthorSerializer, CategorySerializer, BookSerializer
from .filters import BookFilter
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookForm, BookFilterForm
from django.db.models import Q


@login_required
def add_book_page(request):
    if request.user.role not in ['LIBRARIAN', 'SUPERADMIN']:
        return render(request, 'catalog/not_authorized.html')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book-list-page')
    else:
        form = BookForm()

    return render(request, 'catalog/add_book.html', {'form': form})


def book_detail_page(request, pk):
    book = get_object_or_404(Book.objects.select_related('author', 'category'), pk=pk)
    return render(request, 'catalog/book_detail.html', {'book': book})


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLibrarianOrSuperAdmin()]
        return [IsAuthenticatedOrReadOnly()]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLibrarianOrSuperAdmin()]
        return [IsAuthenticatedOrReadOnly()]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author', 'category').all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'isbn', 'author__name', 'category__name', 'description']
    ordering_fields = ['title', 'published_date', 'total_copies', 'available_copies']
    ordering = ['title']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLibrarianOrSuperAdmin()]
        return [IsAuthenticatedOrReadOnly()]


def book_list_page(request):
    """Book list view with advanced filtering and search"""
    books = Book.objects.select_related('author', 'category').all()
    filter_form = BookFilterForm(request.GET or None)
    
    # Handle search/filter parameters
    if request.GET:
        # Text search
        search_query = request.GET.get('search', '').strip()
        if search_query:
            books = books.filter(
                Q(title__icontains=search_query) |
                Q(author__name__icontains=search_query) |
                Q(isbn__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Category filter
        category_id = request.GET.get('category')
        if category_id:
            books = books.filter(category_id=category_id)
        
        # Author filter
        author_id = request.GET.get('author')
        if author_id:
            books = books.filter(author_id=author_id)
        
        # Available only filter
        available_only = request.GET.get('available_only')
        if available_only:
            books = books.filter(available_copies__gt=0)
        
        # Date range filters
        published_from = request.GET.get('published_from')
        if published_from:
            books = books.filter(published_date__gte=published_from)
        
        published_to = request.GET.get('published_to')
        if published_to:
            books = books.filter(published_date__lte=published_to)
        
        # Sorting
        sort_by = request.GET.get('sort_by', 'title')
        if sort_by:
            books = books.order_by(sort_by)
    else:
        books = books.order_by('title')
    
    context = {
        'books': books,
        'filter_form': filter_form,
        'total_books': books.count(),
    }
    
    return render(request, 'catalog/book_list.html', context)


