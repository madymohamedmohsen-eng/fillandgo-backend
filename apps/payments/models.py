from django.db import models
from rest_framework import serializers, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('banque_misr', 'Banque Misr'),
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash'),
        ('wallet', 'App Wallet'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    ENTITY_TYPES = [
        ('booking', 'Fuel Booking'),
        ('mobile_service', 'Mobile Service'),
        ('roadside', 'Roadside Assistance'),
        ('wallet_topup', 'Wallet Top-Up'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='payments')
    entity_type = models.CharField(max_length=30, choices=ENTITY_TYPES)
    entity_id = models.PositiveIntegerField()
    amount_egp = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=30, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_ref = models.CharField(max_length=100, unique=True, null=True, blank=True)
    platform_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # our percentage
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.transaction_ref} - {self.amount_egp} EGP ({self.status})"


class Wallet(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError('Insufficient wallet balance.')
        self.balance -= amount
        self.save()

    def __str__(self):
        return f"{self.user}'s Wallet - {self.balance} EGP"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('user', 'status', 'transaction_ref', 'platform_fee', 'created_at')


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance', 'updated_at')


class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')


class WalletView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        return Response(WalletSerializer(wallet).data)


class WalletTopUpView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        amount = request.data.get('amount')
        method = request.data.get('method', 'banque_misr')
        if not amount or float(amount) <= 0:
            return Response({'detail': 'Invalid amount.'}, status=400)
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        wallet.deposit(float(amount))
        import uuid
        Payment.objects.create(
            user=request.user,
            entity_type='wallet_topup',
            entity_id=wallet.id,
            amount_egp=amount,
            method=method,
            status='success',
            transaction_ref=str(uuid.uuid4()),
        )
        return Response({'detail': f'{amount} EGP added to wallet.', 'new_balance': wallet.balance})
