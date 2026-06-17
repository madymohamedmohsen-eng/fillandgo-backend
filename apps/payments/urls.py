from django.urls import path
from .models import PaymentHistoryView, WalletView, WalletTopUpView

urlpatterns = [
    path('history/',     PaymentHistoryView.as_view(), name='payment_history'),
    path('wallet/',      WalletView.as_view(),         name='wallet'),
    path('wallet/topup/', WalletTopUpView.as_view(),   name='wallet_topup'),
]
