from django.urls import path
from apps.account.views import *
urlpatterns = [
    path('api/get-token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/customer/', RegisterCustomerView.as_view(), name='register_customer'),
    path('api/register/vendor/', RegisterVendorView.as_view(), name='register_vendor'),
    path('api/update-image/customer', UpdateCustomerAvatarView.as_view(), name='update-img-customer'),
    path('api/update-image/vendor', UpdateVendorLogoView.as_view(), name='update-img-vendor'),
]