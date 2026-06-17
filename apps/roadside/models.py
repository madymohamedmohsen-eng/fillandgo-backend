from django.db import models
from rest_framework import serializers, generics, permissions


class RoadsideRequest(models.Model):
    SERVICE_TYPES = [
        ('fuel_delivery', 'Emergency Fuel Delivery'),
        ('towing', 'Towing Service'),
        ('jump_start', 'Jump Start'),
        ('flat_tyre', 'Flat Tyre Assistance'),
        ('lockout', 'Lockout Assistance'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Technician Assigned'),
        ('on_the_way', 'On The Way'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='roadside_requests')
    vehicle = models.ForeignKey('users.Vehicle', on_delete=models.SET_NULL, null=True)
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address_description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    estimated_arrival_minutes = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.user} ({self.status})"


class RoadsideRequestSerializer(serializers.ModelSerializer):
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = RoadsideRequest
        fields = '__all__'
        read_only_fields = ('user', 'status', 'estimated_arrival_minutes', 'price', 'created_at', 'resolved_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class RoadsideListCreateView(generics.ListCreateAPIView):
    serializer_class = RoadsideRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return RoadsideRequest.objects.filter(user=self.request.user).order_by('-created_at')


class RoadsideDetailView(generics.RetrieveAPIView):
    serializer_class = RoadsideRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return RoadsideRequest.objects.filter(user=self.request.user)
