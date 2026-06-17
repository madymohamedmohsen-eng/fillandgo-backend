from django.urls import path
from .views import StationListView, StationDetailView, StationSlotsView, StationReviewCreateView

urlpatterns = [
    path('',                   StationListView.as_view(),         name='station_list'),
    path('<int:pk>/',          StationDetailView.as_view(),       name='station_detail'),
    path('<int:pk>/slots/',    StationSlotsView.as_view(),        name='station_slots'),
    path('<int:pk>/reviews/',  StationReviewCreateView.as_view(), name='station_review'),
]
