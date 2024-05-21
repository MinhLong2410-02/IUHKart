from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.account.models import User, Customer, Vendor
from apps.account.serializers import UserSerializer, CustomerSerializer, VendorSerializer, MyTokenObtainPairSerializer

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
