from django import forms
from .models import Book, Author, Category


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'author', 'category', 'description',
                  'published_date', 'total_copies', 'available_copies', 'cover_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'published_date': forms.DateInput(attrs={'type': 'date'}),
        }


class BookFilterForm(forms.Form):
    """Form for filtering and searching books"""
    
    SORT_CHOICES = [
        ('title', 'Title (A-Z)'),
        ('-title', 'Title (Z-A)'),
        ('-published_date', 'Newest First'),
        ('published_date', 'Oldest First'),
        ('-available_copies', 'Most Available'),
        ('available_copies', 'Least Available'),
    ]
    
    search = forms.CharField(
        required=False,
        label='Search Books',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, author, or ISBN...',
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=False,
        empty_label='All Authors',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    available_only = forms.BooleanField(
        required=False,
        label='Only Available Books',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='title',
        label='Sort By',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    published_from = forms.DateField(
        required=False,
        label='Published From',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    published_to = forms.DateField(
        required=False,
        label='Published To',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )