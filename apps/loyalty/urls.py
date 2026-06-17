from django.urls import path
from .models import LoyaltyAccountView, LoyaltyTransactionListView, RedeemPointsView

urlpatterns = [
    path('',            LoyaltyAccountView.as_view(),        name='loyalty_account'),
    path('history/',    LoyaltyTransactionListView.as_view(), name='loyalty_history'),
    path('redeem/',     RedeemPointsView.as_view(),           name='loyalty_redeem'),
]
