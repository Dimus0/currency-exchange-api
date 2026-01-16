from locale import currency
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions

from api.models import *
from .serializer import RegisterSerializer, CurrencyExchangeSerializer

from api.services.exchange_service import get_exchange_rate

# Create your views here.
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        UserBalance.objects.create(user=user)

        return Response(
            {"message":"User created successfully"}, 
            status=status.HTTP_201_CREATED
        )
    
class CurrencyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        currency_code = request.data.get("currency_code")

        if not currency_code:
            return Response({"Error": " a currency code is required"}, status=400)

        user_balance = request.user.balance
        if user_balance.balance <= 0:
            return Response({"Error" : "User balance is 0"}, status=400)

        rate = get_exchange_rate(currency_code=currency_code)

        exchange = CurrencyExchange.objects.create(
            user=request.user,
            currency_code=currency_code,
            rate=rate
        )

        user_balance.balance -= 1
        user_balance.save()

        serializer = CurrencyExchangeSerializer(exchange)

        return Response(serializer.data, status=200)
    
class BalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        balance = request.user.balance
        return Response({"balance": balance.balance}, status=200)
    
class HistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        exchanges = CurrencyExchange.objects.filter(user=request.user).order_by('-created_at')

        serializer = CurrencyExchangeSerializer(exchanges,many=True)


        return Response(serializer.data, status=200)