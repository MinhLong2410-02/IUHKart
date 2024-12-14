from django.shortcuts import render
from rest_framework import generics, permissions, status
from apps.order.models import Order
from apps.order.serializers import *
from rest_framework.response import Response

class CreateOrderByVendorView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateOrderByVendorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_orders = serializer.save()

        # Prepare the response
        response_data = [
            {
                "order_number": order.order_number,
                "order_total": order.order_total,
                "vendor": order.orderproduct_set.first().product.created_by.name,
                "products": [
                    {
                        "product_name": op.product.product_name,
                        "price": op.price,
                        "quantity": op.quantity,
                    }
                    for op in order.orderproduct_set.all()
                ]
            }
            for order in created_orders
        ]

        return Response(response_data, status=status.HTTP_201_CREATED)


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