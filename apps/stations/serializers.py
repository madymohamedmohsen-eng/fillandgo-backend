from rest_framework import serializers
from .models import Station, FuelType, StationSlot, StationReview
import math


class FuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelType
        fields = ('id', 'fuel_type', 'price_per_liter', 'is_available')


class StationSlotSerializer(serializers.ModelSerializer):
    available_spots = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()

    class Meta:
        model = StationSlot
        fields = ('id', 'date', 'time', 'capacity', 'booked_count', 'available_spots', 'is_available')


class StationReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = StationReview
        fields = ('id', 'user_name', 'rating', 'comment', 'created_at')
        read_only_fields = ('user_name', 'created_at')

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class StationListSerializer(serializers.ModelSerializer):
    fuel_types = FuelTypeSerializer(many=True, read_only=True)
    current_wait_time = serializers.ReadOnlyField()
    distance_km = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = ('id', 'name', 'brand', 'address', 'latitude', 'longitude',
                  'image', 'is_24_hours', 'opening_time', 'closing_time',
                  'fuel_types', 'current_wait_time', 'distance_km', 'average_rating')

    def get_distance_km(self, obj):
        user_lat = self.context.get('user_lat')
        user_lng = self.context.get('user_lng')
        if not user_lat or not user_lng:
            return None
        # Haversine formula
        R = 6371
        lat1, lon1 = math.radians(float(user_lat)), math.radians(float(user_lng))
        lat2, lon2 = math.radians(float(obj.latitude)), math.radians(float(obj.longitude))
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return round(R * 2 * math.asin(math.sqrt(a)), 2)

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / len(reviews), 1)


class StationDetailSerializer(StationListSerializer):
    slots = StationSlotSerializer(many=True, read_only=True)
    reviews = StationReviewSerializer(many=True, read_only=True)

    class Meta(StationListSerializer.Meta):
        fields = StationListSerializer.Meta.fields + ('slots', 'reviews', 'phone_number')
