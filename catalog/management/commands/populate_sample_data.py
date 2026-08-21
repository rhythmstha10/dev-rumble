from django.core.management.base import BaseCommand
from catalog.models import Author, Category, Book
from datetime import datetime
import random


class Command(BaseCommand):
    help = 'Populate the database with sample books, authors, and categories'

    def handle(self, *args, **options):
        # Create Categories
        categories_data = [
            {'name': 'Fiction', 'description': 'Fictional stories and novels'},
            {'name': 'Non-Fiction', 'description': 'Educational and factual books'},
            {'name': 'Science', 'description': 'Science and technology books'},
            {'name': 'History', 'description': 'Historical accounts and narratives'},
            {'name': 'Biography', 'description': 'Life stories and memoirs'},
            {'name': 'Mystery', 'description': 'Mystery and thriller novels'},
            {'name': 'Romance', 'description': 'Romantic fiction'},
            {'name': 'Poetry', 'description': 'Poetry collections'},
            {'name': 'Self-Help', 'description': 'Personal development books'},
            {'name': 'Children', 'description': 'Books for children'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Create Authors
        authors_data = [
            'J.K. Rowling',
            'George R.R. Martin',
            'J.R.R. Tolkien',
            'Stephen King',
            'Haruki Murakami',
            'Margaret Atwood',
            'Chimamanda Ngozi Adichie',
            'Paulo Coelho',
            'Neil Gaiman',
            'Agatha Christie',
            'Sherlock Doyle',
            'Jane Austen',
            'Charlotte Brontë',
            'F. Scott Fitzgerald',
            'Ernest Hemingway',
            'Maya Angelou',
            'Malcolm Gladwell',
            'Yuval Noah Harari',
            'Simon Sinek',
            'Brené Brown',
        ]

        authors = {}
        for author_name in authors_data:
            author, created = Author.objects.get_or_create(name=author_name)
            authors[author_name] = author
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created author: {author.name}'))

        # Create Books
        books_data = [
            {
                'title': "Harry Potter and the Philosopher's Stone",
                'isbn': '9780747532699',
                'author': 'J.K. Rowling',
                'category': 'Fiction',
                'description': 'The first Harry Potter book follows young wizard Harry Potter.',
                'published_date': '1997-06-26',
                'total_copies': 5,
            },
            {
                'title': 'A Game of Thrones',
                'isbn': '9780553103540',
                'author': 'George R.R. Martin',
                'category': 'Fiction',
                'description': 'The first book of A Song of Ice and Fire series.',
                'published_date': '1996-08-01',
                'total_copies': 4,
            },
            {
                'title': 'The Hobbit',
                'isbn': '9780547928227',
                'author': 'J.R.R. Tolkien',
                'category': 'Fiction',
                'description': 'A fantasy adventure following Bilbo Baggins.',
                'published_date': '1937-09-21',
                'total_copies': 6,
            },
            {
                'title': 'The Shining',
                'isbn': '9780385333312',
                'author': 'Stephen King',
                'category': 'Mystery',
                'description': 'A psychological horror novel set in an isolated hotel.',
                'published_date': '1977-01-28',
                'total_copies': 3,
            },
            {
                'title': 'Norwegian Wood',
                'isbn': '9780099532522',
                'author': 'Haruki Murakami',
                'category': 'Fiction',
                'description': 'A coming-of-age story set in 1987 Tokyo.',
                'published_date': '1987-09-04',
                'total_copies': 4,
            },
            {
                'title': 'The Handmaid\'s Tale',
                'isbn': '9780385490818',
                'author': 'Margaret Atwood',
                'category': 'Fiction',
                'description': 'Dystopian novel set in the Republic of Gilead.',
                'published_date': '1985-06-01',
                'total_copies': 5,
            },
            {
                'title': 'Half of a Yellow Sun',
                'isbn': '9780007150960',
                'author': 'Chimamanda Ngozi Adichie',
                'category': 'Fiction',
                'description': 'Novel set during the Biafran War in Nigeria.',
                'published_date': '2006-09-28',
                'total_copies': 3,
            },
            {
                'title': 'The Alchemist',
                'isbn': '9780062412928',
                'author': 'Paulo Coelho',
                'category': 'Self-Help',
                'description': 'Philosophical novel about following your dreams.',
                'published_date': '1988-01-01',
                'total_copies': 7,
            },
            {
                'title': 'American Gods',
                'isbn': '9780060565671',
                'author': 'Neil Gaiman',
                'category': 'Fiction',
                'description': 'Modern fantasy novel exploring American mythology.',
                'published_date': '2001-06-19',
                'total_copies': 4,
            },
            {
                'title': 'Murder on the Orient Express',
                'isbn': '9780062073556',
                'author': 'Agatha Christie',
                'category': 'Mystery',
                'description': 'A classic detective mystery featuring Hercule Poirot.',
                'published_date': '1934-01-01',
                'total_copies': 5,
            },
            {
                'title': 'A Study in Scarlet',
                'isbn': '9780486404769',
                'author': 'Sherlock Doyle',
                'category': 'Mystery',
                'description': 'First appearance of Sherlock Holmes.',
                'published_date': '1887-11-01',
                'total_copies': 4,
            },
            {
                'title': 'Pride and Prejudice',
                'isbn': '9780143039990',
                'author': 'Jane Austen',
                'category': 'Romance',
                'description': 'Romantic novel of manners and marriage.',
                'published_date': '1813-01-28',
                'total_copies': 6,
            },
            {
                'title': 'Jane Eyre',
                'isbn': '9780143039999',
                'author': 'Charlotte Brontë',
                'category': 'Romance',
                'description': 'Gothic romance and bildungsroman.',
                'published_date': '1847-10-16',
                'total_copies': 5,
            },
            {
                'title': 'The Great Gatsby',
                'isbn': '9780743273565',
                'author': 'F. Scott Fitzgerald',
                'category': 'Fiction',
                'description': 'Jazz Age novel of wealth and love.',
                'published_date': '1925-04-10',
                'total_copies': 7,
            },
            {
                'title': 'The Old Man and the Sea',
                'isbn': '9780684801223',
                'author': 'Ernest Hemingway',
                'category': 'Fiction',
                'description': 'Novella about an aging fisherman.',
                'published_date': '1952-09-01',
                'total_copies': 4,
            },
            {
                'title': 'I Know Why the Caged Bird Sings',
                'isbn': '9780345514400',
                'author': 'Maya Angelou',
                'category': 'Biography',
                'description': 'Autobiography of Maya Angelou.',
                'published_date': '1969-03-17',
                'total_copies': 3,
            },
            {
                'title': 'Outliers',
                'isbn': '9780316017923',
                'author': 'Malcolm Gladwell',
                'category': 'Non-Fiction',
                'description': 'Exploration of why some people succeed.',
                'published_date': '2008-11-18',
                'total_copies': 5,
            },
            {
                'title': 'Sapiens',
                'isbn': '9780062316097',
                'author': 'Yuval Noah Harari',
                'category': 'History',
                'description': 'Brief history of humankind.',
                'published_date': '2011-09-01',
                'total_copies': 6,
            },
            {
                'title': 'Start With Why',
                'isbn': '9781591846444',
                'author': 'Simon Sinek',
                'category': 'Self-Help',
                'description': 'How great leaders inspire action.',
                'published_date': '2009-10-15',
                'total_copies': 4,
            },
            {
                'title': 'Dare to Lead',
                'isbn': '9780399592522',
                'author': 'Brené Brown',
                'category': 'Self-Help',
                'description': 'Brave work in the arena of life.',
                'published_date': '2018-10-02',
                'total_copies': 5,
            },
        ]

        books_created = 0
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults={
                    'title': book_data['title'],
                    'author': authors[book_data['author']],
                    'category': categories[book_data['category']],
                    'description': book_data['description'],
                    'published_date': book_data['published_date'],
                    'total_copies': book_data['total_copies'],
                    'available_copies': book_data['total_copies'],
                }
            )
            if created:
                books_created += 1
                self.stdout.write(self.style.SUCCESS(f'Created book: {book.title}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully populated database!'))
        self.stdout.write(self.style.SUCCESS(f'  - Categories: {len(categories)}'))
        self.stdout.write(self.style.SUCCESS(f'  - Authors: {len(authors)}'))
        self.stdout.write(self.style.SUCCESS(f'  - Books: {books_created} new books added'))
