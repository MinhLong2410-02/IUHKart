from django.urls import path
from apps.order.views import *
urlpatterns = [
    path('api/create/', CreateOrderView.as_view(), name='create-order'),
    path('api/cancel/', OrderCancelView.as_view(), name='cancel-order'),
]