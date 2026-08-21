from django.core.management.base import BaseCommand
from catalog.models import Book as CatalogBook
from accounts.models import User
from circulation_app.models import Loan as CirculationLoan, Fine
from reservations.models import Reservation
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate circulation_app and reservations with sample data'

    def handle(self, *args, **options):
        # Get sample data
        catalog_books = CatalogBook.objects.all()[:10]
        members = User.objects.filter(role='member')

        if not catalog_books or not members:
            self.stdout.write(self.style.WARNING(
                'Not enough books or members. Please run populate_sample_data first.'
            ))
            return

        loans_created = 0
        fines_created = 0
        reservations_created = 0

        # Create circulation loans
        for idx, member in enumerate(members):
            if idx < len(catalog_books):
                book = catalog_books[idx]
                if book.available_copies > 0:
                    # Create a loan
                    loan, created = CirculationLoan.objects.get_or_create(
                        user=member,
                        book=book,
                        status='borrowed',
                        defaults={
                            'borrow_date': timezone.now() - timedelta(days=5),
                            'due_date': timezone.now() + timedelta(days=9),
                        }
                    )
                    if created:
                        book.available_copies -= 1
                        book.save()
                        loans_created += 1
                        self.stdout.write(self.style.SUCCESS(
                            f'Created circulation loan: {member.username} borrowed "{book.title}"'
                        ))

                        # Add a fine for overdue books (randomly)
                        if idx % 2 == 0:
                            fine, fine_created = Fine.objects.get_or_create(
                                loan=loan,
                                defaults={
                                    'amount': Decimal('50.00'),
                                    'is_paid': False,
                                }
                            )
                            if fine_created:
                                fines_created += 1
                                self.stdout.write(self.style.SUCCESS(
                                    f'Created fine: {member.username} owes ₹{fine.amount}'
                                ))

        # Create reservations
        available_books = CatalogBook.objects.filter(available_copies=0)[:3]
        for idx, book in enumerate(available_books):
            if idx < len(members):
                member = members[(idx + 1) % len(members)]
                reservation, created = Reservation.objects.get_or_create(
                    user=member,
                    book=book,
                    status='PENDING',
                    defaults={
                        'created_at': timezone.now() - timedelta(days=2),
                    }
                )
                if created:
                    reservations_created += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'Created reservation: {member.username} reserved "{book.title}"'
                    ))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully populated circulation and reservations!'))
        self.stdout.write(self.style.SUCCESS(f'  - Circulation Loans: {loans_created} new loans created'))
        self.stdout.write(self.style.SUCCESS(f'  - Fines: {fines_created} new fines created'))
        self.stdout.write(self.style.SUCCESS(f'  - Reservations: {reservations_created} new reservations created'))
