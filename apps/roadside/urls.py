from django.urls import path
from .models import RoadsideListCreateView, RoadsideDetailView

urlpatterns = [
    path('',           RoadsideListCreateView.as_view(), name='roadside_list'),
    path('<int:pk>/',  RoadsideDetailView.as_view(),     name='roadside_detail'),
]
