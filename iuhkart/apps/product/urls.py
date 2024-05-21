from django.urls import path
from apps.product.views import *
urlpatterns = [
    path('api/vendor/', VendorProductListView.as_view(), name='vendor-product-list'),
    path('api/customer/', CustomerProductListView.as_view(), name='customer-product-list'),
]