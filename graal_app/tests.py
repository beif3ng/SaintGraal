from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Transaction
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .serializers import CategorySerializer, TransactionSerializer
from rest_framework.test import APIClient

class ModelTests(TestCase):
    def setUp(self):
        # Создаём тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Создаём тестовую категорию
        self.category = Category.objects.create(user=self.user, name='Food')

    def test_category_creation(self):
        """Тест создания категории."""
        self.assertEqual(self.category.name, 'Food')
        self.assertEqual(self.category.user.username, 'testuser')

    def test_transaction_creation(self):
        """Тест создания транзакции."""
        transaction = Transaction.objects.create(
            user=self.user,
            type='expense',
            category=self.category,
            amount=100.50,
            description='Test transaction'
        )
        self.assertEqual(transaction.type, 'expense')
        self.assertEqual(transaction.amount, 100.50)
        self.assertEqual(transaction.category.name, 'Food')
        self.assertEqual(transaction.user.username, 'testuser')



class SerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(user=self.user, name='Food')

    def test_category_serializer(self):
        """Тест сериализатора категории."""
        serializer = CategorySerializer(instance=self.category)
        self.assertEqual(serializer.data['name'], 'Food')
        self.assertEqual(serializer.data['user'], self.user.id)

    def test_transaction_serializer(self):
        """Тест сериализатора транзакции."""
        transaction = Transaction.objects.create(
            user=self.user,
            type='expense',
            category=self.category,
            amount=100.50,
            description='Test transaction'
        )
        serializer = TransactionSerializer(instance=transaction)
        self.assertEqual(serializer.data['type'], 'expense')
        self.assertEqual(serializer.data['amount'], '100.50')
        self.assertEqual(serializer.data['category'], self.category.id)
        self.assertEqual(serializer.data['user'], self.user.id)

class ViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(user=self.user, name='Food')
        self.client.force_authenticate(user=self.user)

    def test_category_list(self):
        """Тест получения списка категорий."""
        url = reverse('categories')  # Используем правильное имя URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Food')

    def test_transaction_create(self):
        """Тест создания транзакции."""
        url = reverse('transactions')  # Используем правильное имя URL
        data = {
            'type': 'expense',
            'category': self.category.id,
            'amount': 100.50,
            'description': 'Test transaction'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['type'], 'expense')
        self.assertEqual(response.data['amount'], '100.50')
        self.assertEqual(response.data['category'], self.category.id)
        self.assertEqual(response.data['user'], self.user.id)