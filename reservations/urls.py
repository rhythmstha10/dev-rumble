"""
reservations/urls.py

Mount this in the project's root urls.py with:
    path("reservations/", include("reservations.urls")),
"""
from django.urls import path

from . import views

app_name = "reservations"

urlpatterns = [
    path("books/<int:book_id>/reserve/", views.create_reservation_view, name="create"),
    path("<int:pk>/cancel/", views.cancel_reservation_view, name="cancel"),
    path("mine/", views.my_reservations_view, name="my_reservations"),
    path("all/", views.all_reservations_view, name="all"),
]