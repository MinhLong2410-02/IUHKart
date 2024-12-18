from django.urls import path
from apps.account.views import *
urlpatterns = [
    path('api/token/customer/', CustomerTokenObtainPairView.as_view(), name='token_obtain_pair_customer'),
    path('api/token/vendor/', VendorTokenObtainPairView.as_view(), name='token_obtain_pair_vendor'),
    path('api/token/logout/', LogoutView.as_view(), name='logout'),
    path('api/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/customer/', RegisterCustomerView.as_view(), name='register_customer'),
    
    path('api/token-validate/', ValidateTokenView.as_view(), name='token-validate'),
    path('api/vendor/me', VendorDetailView.as_view(), name='vendor-detail'),
    path('api/customer/me', CustomerDetailView.as_view(), name='customer-detail'),

    path('api/register/vendor/', RegisterVendorView.as_view(), name='register_vendor'),
    path('api/update-image/customer/', UpdateCustomerAvatarView.as_view(), name='update-img-customer'),
    path('api/update-image/vendor/', UpdateVendorLogoView.as_view(), name='update-img-vendor'),
    path('api/update-dob/customer/', CustomerUpdateAPIView.as_view(), name='update-dob-customer'),
    path('api/update-bank-account/', UpdateBankAccountView.as_view(), name='update-bank-account'),
    path('api/add-money/', UpdateMoneyView.as_view(), name='update-money'),
]