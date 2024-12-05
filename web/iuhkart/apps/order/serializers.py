from rest_framework import serializers
from apps.order.models import Order, OrderProduct
from apps.product.models import Product
from apps.discount.models import Discount, OrderProductDiscount
from apps.cart.models import CartProduct
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
        fields = ['order_number', 'products', 'order_total']
        read_only_fields = ['order_number', 'order_total']

    @transaction.atomic
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order(
            order_number=str(uuid.uuid4()),  # Generate a unique order number
            customer=self.context['request'].user.customer  # Assign the customer from request user
        )
        total_price = 0.0
        cart = self.context['request'].user.customer.cart
        for product_data in products_data:
            CartProduct.objects.filter(cart=cart, product_id=product_data['product_id']).delete()
            product = Product.objects.get(pk=product_data['product_id'])
            if product.stock < product_data['quantity']:
                raise serializers.ValidationError(f"Product {product.product_name} is out of stock.")
            product.stock -= product_data['quantity']
            product.save()
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
    
        return order
    
class OrderCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_number']

    def update(self, instance, validated_data):
        # Check if the order can be cancelled
        if instance.order_status not in ['pending', 'processing']:
            raise serializers.ValidationError("Order cannot be cancelled in its current state.")
        order_products = OrderProduct.objects.filter(order=instance)
        product_ids = order_products.values_list('product_id', flat=True)
        products = Product.objects.filter(pk__in=product_ids)
        for product in products:
            product.stock += order_products.get(product=product).quantity
            product.save()
            CartProduct.objects.create(
                cart=instance.customer.cart,
                product=product,
                quantity=order_products.get(product=product).quantity
            )
        instance.order_status = 'cancelled'
        instance.save()
        return instance