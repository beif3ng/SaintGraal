from django.urls import path
from .views import CategoryListCreateAPIView, TransactionListCreateAPIView

urlpatterns = [
    path('categories/', CategoryListCreateAPIView .as_view(), name='categories'),
    path('transactions/', TransactionListCreateAPIView.as_view(), name='transactions'),
]