from django.urls import path
from apps.discount.views import *
urlpatterns = [
    path('api/update/<int:product_id>/', DiscountCreateUpdateView.as_view(), name='discount-update'),
    path('api/delete/<int:product_id>/', DiscountDeleteView.as_view(), name='discount-delete'),
    path('api/create/<int:product_id>/product/', CreateDiscountView.as_view(), name='create-discount'),

]