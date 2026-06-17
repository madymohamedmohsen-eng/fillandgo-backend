from django.urls import path
from .models import MobileServiceListCreateView, MobileServiceDetailView

urlpatterns = [
    path('',           MobileServiceListCreateView.as_view(), name='mobile_service_list'),
    path('<int:pk>/',  MobileServiceDetailView.as_view(),     name='mobile_service_detail'),
]
