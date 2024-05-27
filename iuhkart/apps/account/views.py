from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from apps.account.models import User
from apps.account.serializers import *
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterCustomerView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=response.data['user']['email'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'customer': response.data
        }, status=status.HTTP_201_CREATED)
class RegisterVendorView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = VendorSerializer
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=response.data['user']['email'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'vendor': response.data
        }, status=status.HTTP_201_CREATED)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UpdateCustomerAvatarView(generics.UpdateAPIView):
    serializer_class = CustomerAvatarUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.customer
    @extend_schema(
        exclude=True,
        methods=['GET', 'PATCH']
    )
    def patch(self, request, *args, **kwargs):
        pass

class UpdateVendorLogoView(generics.UpdateAPIView):
    serializer_class = VendorLogoUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.vendor
    
    @extend_schema(
        exclude=True,
        methods=['GET', 'PATCH']
    )
    def patch(self, request, *args, **kwargs):
        pass
class CustomerUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerDOBUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.customer
    
    @extend_schema(
        exclude=True,
        methods=['GET', 'PATCH']
    )
    def get(self, request, *args, **kwargs):
        pass

    @extend_schema(
        exclude=True,
        methods=['GET', 'PATCH']
    )
    def patch(self, request, *args, **kwargs):
        pass