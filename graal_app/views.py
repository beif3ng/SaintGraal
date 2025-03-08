from rest_framework import generics, permissions
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer



class CategoryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()



class TransactionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class TransactionRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


