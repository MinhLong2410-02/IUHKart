from django.urls import path, include
from apps.cart.views import CartViewSet, CartDetailsView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('carts/<int:pk>/details/', CartDetailsView.as_view(), name='cart-details'),
]