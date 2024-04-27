# create a new file urls.py in vendor app and add the following code
# """
# URL configuration for vendor app.
# """
from django.urls import path
from .views import *
app_name = 'vendor'

urlpatterns = [
    path('', home, name='home'),
    path('sign-in/', SignInView.as_view(), name='vendor_sign_in'),
    path('add-product/', SignInView.as_view(), name='add_product'),
    path('sign-up/', VendorSignUpView, name='vendor_sign_up'),
]