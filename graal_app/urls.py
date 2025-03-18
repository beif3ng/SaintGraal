from django.urls import path
from .views import CategoryListCreateAPIView, CategoryRetrieveUpdateDeleteAPIView, TransactionListCreateAPIView, TransactionRetrieveUpdateDeleteAPIView

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDeleteAPIView.as_view(), name='category'),
    path('transactions/', TransactionListCreateAPIView.as_view(), name='transactions'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDeleteAPIView.as_view(), name='transaction'),
]


# Add to graal_app/urls.py
from .views import (
    CategorySummaryView, MonthlySummaryView
)
from .export import export_transactions_csv, export_transactions_pdf


urlpatterns += [
    path('analytics/category-summary/', CategorySummaryView.as_view(), name='category-summary'),
    path('analytics/monthly-summary/', MonthlySummaryView.as_view(), name='monthly-summary'),
    path('export/csv/', export_transactions_csv, name='export-csv'),
    path('export/pdf/', export_transactions_pdf, name='export-pdf'),
]