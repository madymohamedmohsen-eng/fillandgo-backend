from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Vehicle
from .serializers import (
    RegisterSerializer, UserProfileSerializer,
    ChangePasswordSerializer, VehicleSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password changed successfully.'})


class VehicleListCreateView(generics.ListCreateAPIView):
    serializer_class = VehicleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)


class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)


class SetPrimaryVehicleView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk, user=request.user)
            vehicle.is_primary = True
            vehicle.save()
            return Response({'detail': 'Primary vehicle updated.'})
        except Vehicle.DoesNotExist:
            return Response({'detail': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)
