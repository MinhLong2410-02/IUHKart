from django.urls import path
from apps.account.views import *
urlpatterns = [
    path('api/get-token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/customer/', RegisterCustomerView.as_view(), name='register_customer'),
    path('api/register/vendor/', RegisterVendorView.as_view(), name='register_vendor'),
]