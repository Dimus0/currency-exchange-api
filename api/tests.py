from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from api.models import CurrencyExchange, UserBalance


class RegisterViewTest(APITestCase):
    """
        Тести для реєстрації користувача
    """
    
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/register/'
    
    def test_register_user_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully')
        self.assertTrue(User.objects.filter(username='testuser').exists())
        
        user = User.objects.get(username='testuser')
        self.assertTrue(UserBalance.objects.filter(user=user).exists())
        self.assertEqual(user.balance.balance, 1000)
    
class CurrencyViewTest(APITestCase):
    """
        Тести для обміну валюти
    """
    
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/currency/'
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.user_balance = UserBalance.objects.create(user=self.user)
        
        self.client.force_authenticate(user=self.user)
            
    def test_currency_exchange_zero_balance(self):
        self.user_balance.balance = 0
        self.user_balance.save()
        
        data = {'currency_code': 'EUR'}
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['Error'], 'User balance is 0')
    
    def test_currency_exchange_unauthenticated(self):
        self.client.force_authenticate(user=None)
        
        data = {'currency_code': 'EUR'}
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BalanceViewTest(APITestCase):
    """
        Тести для перегляду балансу
    """
    
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/balance/'
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.user_balance = UserBalance.objects.create(user=self.user, balance=876)
        
        self.client.force_authenticate(user=self.user)
    
    def test_get_balance_success(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], 876)
    
    def test_get_balance_unauthenticated(self):
        self.client.force_authenticate(user=None)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class HistoryViewTest(APITestCase):
    """
        Тести для перегляду історії 
    """
    
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/history/'
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        UserBalance.objects.create(user=self.user)
        
        self.client.force_authenticate(user=self.user)
    
    def test_get_history_with_exchanges(self):
        CurrencyExchange.objects.create(
            user=self.user,
            currency_code='USD',
            rate=Decimal('42.2345')
        )
        CurrencyExchange.objects.create(
            user=self.user,
            currency_code='EUR',
            rate=Decimal('50.1234')
        )
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['currency_code'], 'EUR')
    
    def test_get_history_empty(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'No exchange history found')
    
    def test_get_history_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)