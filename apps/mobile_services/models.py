from django.db import models
from rest_framework import serializers, generics, permissions
from django.urls import path


# ── Models ──────────────────────────────────────────────────────────────────

class ServiceProvider(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='providers/', null=True, blank=True)
    specializations = models.JSONField(default=list)  # ['oil_change', 'car_wash', ...]
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    is_available = models.BooleanField(default=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name


class MobileServiceRequest(models.Model):
    SERVICE_TYPES = [
        ('oil_change', 'Oil Change'),
        ('car_wash', 'Car Wash at Home'),
        ('tyre_change', 'Tyre Change'),
        ('tyre_inflation', 'Tyre Inflation'),
        ('battery_replacement', 'Battery Replacement'),
        ('basic_inspection', 'Basic Inspection'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('on_the_way', 'On The Way'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='mobile_service_requests')
    vehicle = models.ForeignKey('users.Vehicle', on_delete=models.SET_NULL, null=True)
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPES)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_service_type_display()} for {self.user} on {self.scheduled_time}"


# ── Serializers ──────────────────────────────────────────────────────────────

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'


class MobileServiceRequestSerializer(serializers.ModelSerializer):
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = MobileServiceRequest
        fields = '__all__'
        read_only_fields = ('user', 'provider', 'status', 'created_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


# ── Views ────────────────────────────────────────────────────────────────────

class MobileServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = MobileServiceRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return MobileServiceRequest.objects.filter(user=self.request.user).order_by('-created_at')


class MobileServiceDetailView(generics.RetrieveAPIView):
    serializer_class = MobileServiceRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return MobileServiceRequest.objects.filter(user=self.request.user)


# ── URLs ─────────────────────────────────────────────────────────────────────

urlpatterns = [
    path('',           MobileServiceListCreateView.as_view(), name='mobile_service_list'),
    path('<int:pk>/',  MobileServiceDetailView.as_view(),     name='mobile_service_detail'),
]
