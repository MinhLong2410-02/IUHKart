from rest_framework import serializers
from apps.order.models import Order, OrderProduct
from apps.product.models import Product
from apps.discount.models import Discount
from django.db import transaction
from django.utils import timezone
import uuid
class OrderProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()  # Receive only product_id
    quantity = serializers.IntegerField()
    class Meta:
        model = OrderProduct
        fields = ['product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_number', 'products', 'order_total', 'total_price']
        read_only_fields = ['order_number', 'order_total', 'total_price']

    @transaction.atomic
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(
            order_number=str(uuid.uuid4()),  # Generate a unique order number
            customer=self.context['request'].user.customer  # Assign the customer from request user
        )

        total_price = 0.0
        for product_data in products_data:
            product = Product.objects.get(id=product_data['product_id'])
            discount = Discount.objects.filter(product=product, in_use=True, start_date__lte=timezone.now(), end_date__gte=timezone.now()).first()

            price = product.original_price
            if discount:
                price *= (1 - (discount.discount_percent / 100))
            
            quantity = product_data['quantity']
            OrderProduct.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
            total_price += price * quantity

        order.total_price = total_price
        order.order_total = sum([p['quantity'] for p in products_data])
        order.save()