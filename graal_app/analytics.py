# In a new file: graal_app/analytics.py
import datetime

from django.db.models import Sum

from .models import Transaction


def get_summary_by_category(user, start_date=None, end_date=None):
    """Get spending/income summary grouped by category"""
    query = Transaction.objects.filter(user=user)

    if start_date:
        query = query.filter(created__gte=start_date)
    if end_date:
        query = query.filter(created__lte=end_date)

    expense_summary = query.filter(type='expense').values('category__name').annotate(
        total=Sum('amount')).order_by('-total')

    income_summary = query.filter(type='income').values('category__name').annotate(
        total=Sum('amount')).order_by('-total')

    return {
        'expenses': expense_summary,
        'income': income_summary
    }


def get_monthly_summary(user, year=None):
    """Get monthly spending/income summary"""
    current_year = datetime.datetime.now().year
    year = year or current_year

    results = []
    for month in range(1, 13):
        start_date = datetime.datetime(year, month, 1)
        if month == 12:
            end_date = datetime.datetime(year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            end_date = datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)

        expenses = Transaction.objects.filter(
            user=user, type='expense',
            created__gte=start_date, created__lte=end_date
        ).aggregate(total=Sum('amount'))

        income = Transaction.objects.filter(
            user=user, type='income',
            created__gte=start_date, created__lte=end_date
        ).aggregate(total=Sum('amount'))

        results.append({
            'month': start_date.strftime('%B'),
            'expenses': expenses['total'] or 0,
            'income': income['total'] or 0,
            'savings': (income['total'] or 0) - (expenses['total'] or 0)
        })

    return results