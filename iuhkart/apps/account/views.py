from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from apps.account.models import User
from apps.account.serializers import *

class RegisterCustomerView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        user = serializer.save(user__is_customer=True)

class RegisterVendorView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = VendorSerializer

    def perform_create(self, serializer):
        user = serializer.save(user__is_vendor=True)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UpdateCustomerAvatarView(generics.UpdateAPIView):
    serializer_class = CustomerAvatarUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.customer

class UpdateVendorLogoView(generics.UpdateAPIView):
    serializer_class = VendorLogoUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.vendor