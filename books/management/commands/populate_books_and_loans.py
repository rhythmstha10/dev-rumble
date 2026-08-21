from django.core.management.base import BaseCommand
from books.models import Book as SimpleBook
from accounts.models import User
from loans.models import Loan
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate books app and loans with sample data'

    def handle(self, *args, **options):
        # Create sample books in the books app
        books_data = [
            {'title': 'Python Programming', 'author': 'Guido van Rossum', 'copies': 3},
            {'title': 'JavaScript Essentials', 'author': 'Kyle Simpson', 'copies': 4},
            {'title': 'Django for Beginners', 'author': 'William Vincent', 'copies': 2},
            {'title': 'Clean Code', 'author': 'Robert Martin', 'copies': 5},
            {'title': 'Design Patterns', 'author': 'Gang of Four', 'copies': 3},
            {'title': 'Refactoring', 'author': 'Martin Fowler', 'copies': 2},
            {'title': 'The Pragmatic Programmer', 'author': 'David Thomas', 'copies': 4},
            {'title': 'Code Complete', 'author': 'Steve McConnell', 'copies': 3},
            {'title': 'Introduction to Algorithms', 'author': 'Thomas Cormen', 'copies': 2},
            {'title': 'System Design Interview', 'author': 'Alex Xu', 'copies': 3},
        ]

        books_created = 0
        for book_data in books_data:
            book, created = SimpleBook.objects.get_or_create(
                title=book_data['title'],
                defaults={
                    'author': book_data['author'],
                    'available_copies': book_data['copies'],
                    'hold_copies': 0,
                }
            )
            if created:
                books_created += 1
                self.stdout.write(self.style.SUCCESS(f'Created simple book: {book.title}'))

        # Create sample users if they don't exist
        users_created = 0
        sample_users = [
            {'username': 'member1', 'email': 'member1@library.com', 'first_name': 'John', 'last_name': 'Doe', 'role': 'member'},
            {'username': 'member2', 'email': 'member2@library.com', 'first_name': 'Jane', 'last_name': 'Smith', 'role': 'member'},
            {'username': 'member3', 'email': 'member3@library.com', 'first_name': 'Bob', 'last_name': 'Johnson', 'role': 'member'},
            {'username': 'librarian1', 'email': 'librarian@library.com', 'first_name': 'Alice', 'last_name': 'Wilson', 'role': 'librarian'},
        ]

        for user_data in sample_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'role': user_data['role'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                users_created += 1
                self.stdout.write(self.style.SUCCESS(f'Created user: {user.username} ({user.role})'))

        # Create sample loans
        loans_created = 0
        member_users = User.objects.filter(role='member')[:3]
        simple_books = SimpleBook.objects.all()[:5]

        for idx, member in enumerate(member_users):
            book = simple_books[idx % len(simple_books)]
            if book.available_copies > 0:
                loan, created = Loan.objects.get_or_create(
                    user=member,
                    book=book,
                    status='active',
                    defaults={
                        'due_date': timezone.now() + timedelta(days=14),
                    }
                )
                if created:
                    book.available_copies -= 1
                    book.save()
                    loans_created += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'Created loan: {member.username} borrowed "{book.title}"'
                    ))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully populated books and loans!'))
        self.stdout.write(self.style.SUCCESS(f'  - Simple Books: {books_created} new books added'))
        self.stdout.write(self.style.SUCCESS(f'  - Users: {users_created} new users added'))
        self.stdout.write(self.style.SUCCESS(f'  - Loans: {loans_created} new loans created'))
