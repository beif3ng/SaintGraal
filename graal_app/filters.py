from django_filters import rest_framework as filters
from .models import Category, Transaction


class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['name']


class TransactionFilter(filters.FilterSet):
    type = filters.ChoiceFilter(choices=Transaction.TYPE_CHOICES)
    category = filters.ModelChoiceFilter(queryset=Category.objects.all())
    created = filters.DateFromToRangeFilter()
    amount = filters.RangeFilter()

    class Meta:
        model = Transaction
        fields = ['type', 'category', 'created', 'amount']
