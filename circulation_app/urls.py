from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BorrowBookView, ReturnBookView, RenewLoanView, LoanHistoryView,
    LoanViewSet, FineViewSet
)

router = DefaultRouter()
router.register(r'loans', LoanViewSet, basename='loan')
router.register(r'fines', FineViewSet, basename='fine')

urlpatterns = [
    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('return/', ReturnBookView.as_view(), name='return-book'),
    path('renew/', RenewLoanView.as_view(), name='renew-loan'),
    path('history/', LoanHistoryView.as_view(), name='loan-history'),
    path('', include(router.urls)),
]