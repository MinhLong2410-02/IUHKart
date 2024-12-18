from django.urls import path, include
from apps.cart.views import *

urlpatterns = [
    path('api/add-product/', ProductAddToCartView.as_view(), name='add-product-to-cart'),
    path('api/delete-product/<int:product_id>', ProductDeleteFromCartView.as_view(), name='delete-product-from-cart'),
    path('api/update-product-quantity/<int:product_id>/', ProductQuantityUpdateView.as_view(), name='update-product-quantity'),
    path('api/details/', CartDetailView.as_view(), name='cart-details'),
]