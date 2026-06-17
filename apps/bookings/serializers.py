from rest_framework import serializers, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Booking
from apps.stations.models import StationSlot


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            'station', 'slot', 'vehicle', 'fuel_type',
            'liters_requested', 'amount_egp',
            'scheduled_time', 'payment_method', 'notes'
        )

    def validate(self, data):
        if not data.get('liters_requested') and not data.get('amount_egp'):
            raise serializers.ValidationError('Provide either liters_requested or amount_egp.')
        slot = data.get('slot')
        if slot and not slot.is_available:
            raise serializers.ValidationError('This time slot is fully booked.')
        if data.get('scheduled_time') and data['scheduled_time'] < timezone.now():
            raise serializers.ValidationError('Cannot book a slot in the past.')
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BookingDetailSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source='station.name', read_only=True)
    station_address = serializers.CharField(source='station.address', read_only=True)
    vehicle_info = serializers.SerializerMethodField()
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'

    def get_vehicle_info(self, obj):
        if obj.vehicle:
            return f"{obj.vehicle.year} {obj.vehicle.make} {obj.vehicle.model}"
        return None

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if obj.qr_code and request:
            return request.build_absolute_uri(obj.qr_code.url)
        return None


class BookingListView(generics.ListAPIView):
    serializer_class = BookingDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        qs = Booking.objects.filter(user=self.request.user).select_related('station', 'vehicle')
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs.order_by('-created_at')


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        booking = serializer.save()
        # Award loyalty points
        from apps.loyalty.models import LoyaltyTransaction
        LoyaltyTransaction.objects.create(
            user=booking.user,
            points=10,
            transaction_type='earned',
            description=f'Booking at {booking.station.name}'
        )


class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class CancelBookingView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
            booking.cancel()
            return Response({'detail': 'Booking cancelled successfully.'})
        except Booking.DoesNotExist:
            return Response({'detail': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)
