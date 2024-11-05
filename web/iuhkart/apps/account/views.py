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
        customer_id = response.data['id']
        customer = Customer.objects.select_related('user').get(id=customer_id)
        
        user = customer.user
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
        vendor_id = response.data['id']
        vendor = Vendor.objects.select_related('user').get(id=vendor_id)
        user = vendor.user
        refresh = RefreshToken.for_user(user)
        BankAccount.objects.create(vendor=user.vendor)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'vendor': response.data
        }, status=status.HTTP_201_CREATED)

class CustomerTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomerTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response({'detail': 'Invalid credentials or no customer account associated.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class VendorTokenObtainPairView(TokenObtainPairView):
    serializer_class = VendorTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response({'detail': 'Invalid credentials or no vendor account associated.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
class LogoutView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # try:
        #     refresh_token = request.data.get("refresh")
        #     if not refresh_token:
        #         return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
        #     token = RefreshToken(refresh_token)
        #     token.blacklist()

        #     return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        # except Exception as e:
        #     return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)


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
    
class VendorDetailView(generics.RetrieveAPIView):
    serializer_class = DetailedVendorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.vendor

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CustomerDetailView(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.customer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class UpdateBankAccountView(generics.UpdateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ensure the vendor can only access their own bank account information
        vendor = self.request.user.vendor
        bank_account, _ = BankAccount.objects.get_or_create(vendor=vendor)  # Create if not exists
        return bank_account

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)