from rest_framework import generics, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Station, StationSlot, StationReview
from .serializers import (
    StationListSerializer, StationDetailSerializer,
    StationSlotSerializer, StationReviewSerializer
)


class StationListView(generics.ListAPIView):
    serializer_class = StationListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'brand', 'address')

    def get_queryset(self):
        qs = Station.objects.filter(is_active=True).prefetch_related('fuel_types', 'reviews')
        fuel_type = self.request.query_params.get('fuel_type')
        if fuel_type:
            qs = qs.filter(fuel_types__fuel_type=fuel_type, fuel_types__is_available=True)
        return qs.distinct()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['user_lat'] = self.request.query_params.get('lat')
        ctx['user_lng'] = self.request.query_params.get('lng')
        return ctx


class StationDetailView(generics.RetrieveAPIView):
    queryset = Station.objects.filter(is_active=True).prefetch_related('fuel_types', 'slots', 'reviews')
    serializer_class = StationDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['user_lat'] = self.request.query_params.get('lat')
        ctx['user_lng'] = self.request.query_params.get('lng')
        return ctx


class StationSlotsView(generics.ListAPIView):
    serializer_class = StationSlotSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        station_id = self.kwargs['pk']
        date = self.request.query_params.get('date')
        qs = StationSlot.objects.filter(station_id=station_id)
        if date:
            qs = qs.filter(date=date)
        return qs.order_by('date', 'time')


class StationReviewCreateView(generics.CreateAPIView):
    serializer_class = StationReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            station_id=self.kwargs['pk']
        )

