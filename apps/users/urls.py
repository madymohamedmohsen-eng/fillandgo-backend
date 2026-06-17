from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, UserProfileView,
    ChangePasswordView, VehicleListCreateView,
    VehicleDetailView, SetPrimaryVehicleView
)

urlpatterns = [
    path('register/',           RegisterView.as_view(),          name='register'),
    path('login/',              LoginView.as_view(),              name='login'),
    path('token/refresh/',      TokenRefreshView.as_view(),       name='token_refresh'),
    path('profile/',            UserProfileView.as_view(),        name='profile'),
    path('change-password/',    ChangePasswordView.as_view(),     name='change_password'),
    path('vehicles/',           VehicleListCreateView.as_view(),  name='vehicles'),
    path('vehicles/<int:pk>/',  VehicleDetailView.as_view(),      name='vehicle_detail'),
    path('vehicles/<int:pk>/set-primary/', SetPrimaryVehicleView.as_view(), name='set_primary_vehicle'),
]
