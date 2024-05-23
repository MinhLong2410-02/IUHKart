from django.urls import path
from apps.product.views import *
urlpatterns = [
    path('api/vendor/', VendorProductListView.as_view(), name='vendor-product-list'),
    path('api/customer/', CustomerProductListView.as_view(), name='customer-product-list'),
    path('vendor/create/', VendorProductCreateView.as_view(), name='vendor-product-create'),
    path('vendor/<int:pk>/update/', VendorProductUpdateView.as_view(), name='vendor-product-update'),
    path('vendor/<int:pk>/delete/', VendorProductDeleteView.as_view(), name='vendor-product-delete'),
    path('vendor/<int:product_id>/images/create/', ProductImageCreateView.as_view(), name='product-image-create'),
    path('vendor/<int:product_id>/images/update/<int:pk>/', ProductImageUpdateView.as_view(), name='product-image-update'),
    path('vendor/<int:product_id>/images/delete/<int:pk>/', ProductImageDeleteView.as_view(), name='product-image-delete'),
    path('vendor/<int:product_id>/images/bulk/', ProductImageBulkUpdateCreateView.as_view(), name='product-image-bulk'),
]