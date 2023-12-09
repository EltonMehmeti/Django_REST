# investment/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoanUploadView,
    CashFlowUploadView,
    LoanDetailView,
    CashFlowDetailView,
    RealizedAmountView,
    GrossExpectedAmountView,
    RemainingInvestedAmountView,
    ClosingDateView,
    LoanViewSet,
    CashFlowViewSet,
    ExportLoansCSV,
    ExportCashflowsCSV,
)

router = DefaultRouter()
router.register(r'loans', LoanViewSet)
router.register(r'cashflows', CashFlowViewSet)

urlpatterns = [
    path('api/loan/upload/', LoanUploadView.as_view(), name='loan-upload'),
    path('api/cashflow/upload/', CashFlowUploadView.as_view(), name='cashflow-upload'),
    path('loans/<str:loan_id>/', LoanDetailView.as_view(), name='loan-detail'),
    path('cashflows/<str:cashflow_id>/', CashFlowDetailView.as_view(), name='cashflow-detail'),
    path('realized-amount/<str:loan_id>/', RealizedAmountView.as_view(), name='realized-amount'),
    path('gross-expected-amount/<str:loan_id>/', GrossExpectedAmountView.as_view(), name='gross-expected-amount'),
    path('remaining-invested-amount/<str:loan_id>/', RemainingInvestedAmountView.as_view(), name='remaining-invested-amount'),
    path('closing-date/<str:loan_id>/', ClosingDateView.as_view(), name='closing-date'),
    path('', include(router.urls)),
    path('export/loans/', ExportLoansCSV.as_view(), name='export-to-excel'),
    path('export/cashflows/', ExportCashflowsCSV.as_view(), name='export-to-excel'),

]
