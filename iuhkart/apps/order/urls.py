from django.urls import path
from apps.order.views import *
urlpatterns = [
    path('api/create/', CreateOrderView.as_view(), name='create-order'),
]