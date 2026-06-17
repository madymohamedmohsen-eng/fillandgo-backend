from django.urls import path
from .models import ReminderListCreateView, ReminderDetailView

urlpatterns = [
    path('',           ReminderListCreateView.as_view(), name='reminder_list'),
    path('<int:pk>/',  ReminderDetailView.as_view(),     name='reminder_detail'),
]
