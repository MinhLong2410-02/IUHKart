# create a new file urls.py in vendor app and add the following code
# """
# URL configuration for vendor app.
# """
from django.urls import path
from django.contrib.auth import views as auth_views
from apps.vendor.views import *
app_name = 'vendor'

urlpatterns = [
    path('', home, name='home'),
    path('sign-in/', SignInView.as_view(), name='vendor_sign_in'),
    path('add-product/', SignInView.as_view(), name='add_product'),
    path('becoming-a-member/', VendorSignUpView, name='vendor_sign_up'),
    path(
        "sign-out",
        auth_views.LogoutView.as_view(template_name="sign_out.html"),
        name="vendor_sign_out",
    ),
    path('add-product', product_views.create_product_view, name='add_product'),
    path('edit/<int:product_id>', product_views.edit_product_view, name='edit_product'),
]