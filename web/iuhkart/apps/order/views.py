from django.shortcuts import render
from rest_framework import generics, permissions, status
from apps.order.models import Order
from apps.order.serializers import OrderSerializer, OrderCancelSerializer
from rest_framework.response import Response
class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

class OrderCancelView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCancelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        order = self.get_object()

        # Ensure that the customer requesting the cancellation owns the order
        if order.customer != request.user.customer:
            return Response({"detail": "Permission denied. You can only cancel your own orders."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Order has been cancelled."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)