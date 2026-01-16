from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import *

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CurrencyExchangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyExchange
        fields = ['currency_code', 'rate','created_at']