from django.db import models
from rest_framework import serializers, generics, permissions


class VehicleReminder(models.Model):
    REMINDER_TYPES = [
        ('oil_change', 'Oil Change'),
        ('licence_renewal', 'License Renewal'),
        ('insurance_renewal', 'Insurance Renewal'),
        ('inspection', 'Vehicle Inspection'),
        ('tyre_rotation', 'Tyre Rotation'),
        ('custom', 'Custom Reminder'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reminders')
    vehicle = models.ForeignKey('users.Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    reminder_type = models.CharField(max_length=30, choices=REMINDER_TYPES)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    notify_days_before = models.PositiveIntegerField(default=7)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('due_date',)

    def __str__(self):
        return f"{self.title} - {self.user} (due {self.due_date})"


class VehicleReminderSerializer(serializers.ModelSerializer):
    reminder_type_display = serializers.CharField(source='get_reminder_type_display', read_only=True)
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = VehicleReminder
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

    def get_is_overdue(self, obj):
        from django.utils import timezone
        return not obj.is_completed and obj.due_date < timezone.now().date()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReminderListCreateView(generics.ListCreateAPIView):
    serializer_class = VehicleReminderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        qs = VehicleReminder.objects.filter(user=self.request.user)
        if self.request.query_params.get('pending') == 'true':
            qs = qs.filter(is_completed=False)
        return qs


class ReminderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleReminderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return VehicleReminder.objects.filter(user=self.request.user)
