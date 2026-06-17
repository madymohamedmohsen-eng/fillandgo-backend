from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return f"{self.get_full_name()} ({self.phone_number})"


class Vehicle(models.Model):
    FUEL_TYPES = [
        ('92', 'Octane 92'),
        ('95', 'Octane 95'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    tank_capacity = models.DecimalField(max_digits=5, decimal_places=1, help_text='Liters')
    color = models.CharField(max_length=50, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_primary:
            Vehicle.objects.filter(user=self.user, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.license_plate}"
