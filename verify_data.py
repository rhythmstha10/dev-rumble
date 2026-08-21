#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'circulation.settings')
django.setup()

from catalog.models import Author, Category, Book as CatalogBook
from books.models import Book as SimpleBook
from accounts.models import User
from loans.models import Loan
from circulation_app.models import Loan as CirculationLoan, Fine
from reservations.models import Reservation

print("\n" + "="*50)
print("DATABASE POPULATION VERIFICATION")
print("="*50 + "\n")

print(f"📚 Authors: {Author.objects.count()}")
print(f"📂 Categories: {Category.objects.count()}")
print(f"📖 Catalog Books: {CatalogBook.objects.count()}")
print(f"📕 Simple Books: {SimpleBook.objects.count()}")
print(f"👥 Users: {User.objects.count()}")
print(f"🔄 Loans (books app): {Loan.objects.count()}")
print(f"📋 Circulation Loans: {CirculationLoan.objects.count()}")
print(f"💰 Fines: {Fine.objects.count()}")
print(f"🔐 Reservations: {Reservation.objects.count()}")

print("\n" + "-"*50)
print("SAMPLE CATALOG BOOKS")
print("-"*50 + "\n")

for i, book in enumerate(CatalogBook.objects.all()[:5], 1):
    print(f"{i}. {book.title}")
    print(f"   Author: {book.author.name}")
    print(f"   Category: {book.category.name}")
    print(f"   Copies: {book.available_copies}/{book.total_copies} available")
    print()

print("-"*50)
print("SAMPLE USERS")
print("-"*50 + "\n")

for i, user in enumerate(User.objects.all(), 1):
    print(f"{i}. {user.username} - {user.get_full_name()}")
    print(f"   Role: {user.role}")
    print(f"   Email: {user.email}")
    print()

print("-"*50)
print("ACTIVE LOANS")
print("-"*50 + "\n")

active_loans = CirculationLoan.objects.filter(status='borrowed')
for i, loan in enumerate(active_loans, 1):
    print(f"{i}. {loan.user.username} borrowed '{loan.book.title}'")
    print(f"   Due: {loan.due_date.strftime('%Y-%m-%d')}")
    print()

print("="*50)
print("✓ VERIFICATION COMPLETE")
print("="*50 + "\n")
