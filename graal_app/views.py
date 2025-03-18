from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filters import CategoryFilter, TransactionFilter
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilter

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionFilter

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


# Add to graal_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .analytics import get_summary_by_category, get_monthly_summary


class CategorySummaryView(APIView):
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        summary = get_summary_by_category(request.user, start_date, end_date)
        return Response(summary)


class MonthlySummaryView(APIView):
    def get(self, request):
        year = request.query_params.get('year')
        if year:
            year = int(year)

        summary = get_monthly_summary(request.user, year)
        return Response(summary)