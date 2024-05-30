from django.shortcuts import render
from rest_framework import generics, permissions
from apps.order.models import Order
from apps.order.serializers import OrderSerializer
# Create your views here.
class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)