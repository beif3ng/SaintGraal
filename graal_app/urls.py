from django.urls import path
from .views import CategoryListCreateAPIView, CategoryRetrieveUpdateDeleteAPIView, TransactionListCreateAPIView, TransactionRetrieveUpdateDeleteAPIView

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDeleteAPIView.as_view(), name='category'),
    path('transactions/', TransactionListCreateAPIView.as_view(), name='transactions'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDeleteAPIView.as_view(), name='transaction'),
]
