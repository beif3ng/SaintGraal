# In a new file: graal_app/export.py
import csv
from io import BytesIO

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from .models import Transaction


def export_transactions_csv(request):
    user = request.user
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description'])

    transactions = Transaction.objects.filter(user=user)
    for transaction in transactions:
        writer.writerow([
            transaction.created.strftime('%Y-%m-%d'),
            transaction.get_type_display(),
            transaction.category.name if transaction.category else 'Uncategorized',
            transaction.amount,
            transaction.description
        ])

    return response


def export_transactions_pdf(request):
    user = request.user
    buffer = BytesIO()

    # Set up PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Create table data
    data = [['Date', 'Type', 'Category', 'Amount', 'Description']]

    transactions = Transaction.objects.filter(user=user)
    for transaction in transactions:
        data.append([
            transaction.created.strftime('%Y-%m-%d'),
            transaction.get_type_display(),
            transaction.category.name if transaction.category else 'Uncategorized',
            str(transaction.amount),
            transaction.description
        ])

    # Create table and style
    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    elements.append(table)

    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    # Return PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'
    response.write(pdf)

    return response