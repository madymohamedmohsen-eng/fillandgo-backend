from django.db import models
import uuid
import qrcode
import io
from django.core.files.base import ContentFile


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('banque_misr', 'Banque Misr'),
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('wallet', 'App Wallet'),
    ]

    booking_ref = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey('users.Vehicle', on_delete=models.SET_NULL, null=True)
    station = models.ForeignKey('stations.Station', on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey('stations.StationSlot', on_delete=models.SET_NULL, null=True, related_name='bookings')
    fuel_type = models.CharField(max_length=20)
    liters_requested = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    amount_egp = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='cash')
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    cars_ahead = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            self._generate_qr_code()
            self._update_slot_count()

    def _generate_qr_code(self):
        qr_data = f"FILLANDGO|{self.booking_ref}|{self.station.name}|{self.scheduled_time}"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        filename = f"qr_{self.booking_ref}.png"
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=True)

    def _update_slot_count(self):
        if self.slot:
            self.slot.booked_count += 1
            self.slot.save()
            self.cars_ahead = self.slot.booked_count - 1
            Booking.objects.filter(pk=self.pk).update(cars_ahead=self.cars_ahead)

    def cancel(self):
        if self.status in ('pending', 'confirmed'):
            self.status = 'cancelled'
            self.save()
            if self.slot:
                self.slot.booked_count = max(0, self.slot.booked_count - 1)
                self.slot.save()

    def __str__(self):
        return f"Booking {self.booking_ref} - {self.user} @ {self.station}"
