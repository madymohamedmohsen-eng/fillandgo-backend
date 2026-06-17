from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)  # e.g. Total, Misr Petroleum
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    phone_number = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='stations/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_24_hours = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.address}"

    @property
    def current_wait_time(self):
        """Returns estimated wait time in minutes based on active bookings."""
        from apps.bookings.models import Booking
        from django.utils import timezone
        now = timezone.now()
        active_count = Booking.objects.filter(
            station=self,
            scheduled_time__date=now.date(),
            scheduled_time__hour=now.hour,
            status='confirmed'
        ).count()
        return active_count * 3  # ~3 min per car


class FuelType(models.Model):
    FUEL_CHOICES = [
        ('92', 'Octane 92'),
        ('95', 'Octane 95'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric Charging'),
    ]
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='fuel_types')
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    price_per_liter = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('station', 'fuel_type')

    def __str__(self):
        return f"{self.station.name} - {self.get_fuel_type_display()} @ {self.price_per_liter} EGP"


class StationSlot(models.Model):
    """Time slots available for booking at a station."""
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    time = models.TimeField()
    capacity = models.PositiveIntegerField(default=5)  # cars per slot
    booked_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('station', 'date', 'time')

    @property
    def available_spots(self):
        return self.capacity - self.booked_count

    @property
    def is_available(self):
        return self.booked_count < self.capacity

    def __str__(self):
        return f"{self.station.name} | {self.date} {self.time} ({self.available_spots} spots)"


class StationReview(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('station', 'user')
