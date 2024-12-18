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
                "order_id": order.order_id,
                "order_number": order.order_number,
                "order_total": order.order_total,
                "vendor": order.orderproduct_set.first().product.created_by.name,
                "products": [
                    {
                        "product_name": op.product.product_name,
                        "price": op.price,
                        "quantity": op.quantity,
                        "image_url": op.product.images.filter(is_main=True).first().image_url.url
                        if op.product.images.filter(is_main=True).exists()
                        else None,
                    }
                    for op in order.orderproduct_set.all()
                ]
            }
            for order in created_orders
        ]

        return Response(response_data, status=status.HTTP_201_CREATED)

class ProcessTransactionView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProcessTransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transactions = serializer.save()

        # Prepare the response
        response_data = [
            {
                "transaction_id": transaction.transaction_id,
                "order_id": transaction.order.order_id,
                "total_money": transaction.total_money,
                "status": transaction.status,
            }
            for transaction in transactions
        ]

        return Response(response_data, status=status.HTTP_201_CREATED)
