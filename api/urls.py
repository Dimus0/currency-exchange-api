from django.urls import path
from .views import RegisterView,CurrencyView,BalanceView,HistoryView,CurrenciesConvertView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('currency/',CurrencyView.as_view(),name="currency"),
    path('balance/',BalanceView.as_view(),name="balance"),
    path('history/',HistoryView.as_view(),name="history"),
    path('convert/',CurrenciesConvertView.as_view(),name="currency-convert"),
]

