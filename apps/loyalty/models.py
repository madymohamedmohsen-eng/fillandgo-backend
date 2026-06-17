from django.db import models
from rest_framework import serializers, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


class LoyaltyAccount(models.Model):
    TIERS = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='loyalty_account')
    points = models.PositiveIntegerField(default=0)
    tier = models.CharField(max_length=20, choices=TIERS, default='bronze')
    total_points_earned = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def add_points(self, amount):
        self.points += amount
        self.total_points_earned += amount
        self._update_tier()
        self.save()

    def redeem_points(self, amount):
        if self.points < amount:
            raise ValueError('Insufficient points.')
        self.points -= amount
        self.save()

    def _update_tier(self):
        if self.total_points_earned >= 5000:
            self.tier = 'platinum'
        elif self.total_points_earned >= 2000:
            self.tier = 'gold'
        elif self.total_points_earned >= 500:
            self.tier = 'silver'
        else:
            self.tier = 'bronze'

    def __str__(self):
        return f"{self.user} - {self.tier.capitalize()} ({self.points} pts)"


class LoyaltyTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('earned', 'Earned'),
        ('redeemed', 'Redeemed'),
        ('expired', 'Expired'),
        ('bonus', 'Bonus'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='loyalty_transactions')
    points = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        account, _ = LoyaltyAccount.objects.get_or_create(user=self.user)
        if self.transaction_type in ('earned', 'bonus'):
            account.add_points(self.points)
        elif self.transaction_type == 'redeemed':
            account.redeem_points(self.points)


class LoyaltyAccountSerializer(serializers.ModelSerializer):
    tier_display = serializers.CharField(source='get_tier_display', read_only=True)
    next_tier_points = serializers.SerializerMethodField()

    class Meta:
        model = LoyaltyAccount
        fields = ('points', 'tier', 'tier_display', 'total_points_earned', 'next_tier_points', 'updated_at')

    def get_next_tier_points(self, obj):
        thresholds = {'bronze': 500, 'silver': 2000, 'gold': 5000, 'platinum': None}
        return thresholds.get(obj.tier)


class LoyaltyTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyTransaction
        fields = '__all__'
        read_only_fields = ('user', 'created_at')


class LoyaltyAccountView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        account, _ = LoyaltyAccount.objects.get_or_create(user=request.user)
        return Response(LoyaltyAccountSerializer(account).data)


class LoyaltyTransactionListView(generics.ListAPIView):
    serializer_class = LoyaltyTransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return LoyaltyTransaction.objects.filter(user=self.request.user).order_by('-created_at')


class RedeemPointsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        points = request.data.get('points')
        if not points or int(points) <= 0:
            return Response({'detail': 'Invalid points amount.'}, status=400)
        try:
            LoyaltyTransaction.objects.create(
                user=request.user,
                points=int(points),
                transaction_type='redeemed',
                description='Points redeemed by user'
            )
            return Response({'detail': f'{points} points redeemed successfully.'})
        except ValueError as e:
            return Response({'detail': str(e)}, status=400)
