from django.urls import path
from .views import RegisterView, LoginView, ProfileView, LibrarianOnlyTestView, PasswordResetRequestView, PasswordResetConfirmView, register_page, login_page, profile_page, logout_page, password_reset_request_page, password_reset_confirm_page, dashboard_page, AdminStatsView, my_books_page, reservations_page, campus_ai_page, study_planner_page, announcements_page, fines_page

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('test-librarian/', LibrarianOnlyTestView.as_view(), name='test-librarian'),
    path('admin-stats/', AdminStatsView.as_view(), name='admin-stats'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('register-page/', register_page, name='register-page'),
    path('login-page/', login_page, name='login-page'),
    path('profile-page/', profile_page, name='profile-page'),
    path('logout-page/', logout_page, name='logout-page'),
    path('password-reset-page/', password_reset_request_page, name='password-reset-page'),
    path('password-reset-confirm-page/', password_reset_confirm_page, name='password-reset-confirm-page'),
    path('dashboard-page/', dashboard_page, name='dashboard-page'),
    path('my-books-page/', my_books_page, name='my-books-page'),
    path('reservations-page/', reservations_page, name='reservations-page'),
    path('campus-ai-page/', campus_ai_page, name='campus-ai-page'),
    path('study-planner-page/', study_planner_page, name='study-planner-page'),
    path('announcements-page/', announcements_page, name='announcements-page'),
    path('fines-page/', fines_page, name='fines-page'),
]
