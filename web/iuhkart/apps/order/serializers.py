from rest_framework import serializers
from apps.account.models import Customer
from apps.order.models import Order, OrderProduct
from apps.product.models import Product
from apps.discount.models import Discount, OrderProductDiscount
from apps.cart.models import CartProduct
from django.db import transaction
from django.db.models import Max
from django.utils import timezone
from uuid import uuid4

class VendorOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_number', 'order_total', 'order_status']

class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'original_price', 'stock']
        
        
class CreateOrderByVendorSerializer(serializers.Serializer):
    products = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
            help_text="A list of products with product_id and quantity."
        ),
        allow_empty=False,
        help_text="A list of objects containing product_id and quantity."
    )

    def validate(self, data):
        product_ids = [item['product_id'] for item in data['products']]
        products = Product.objects.filter(product_id__in=product_ids)
        if len(products) != len(product_ids):
            raise serializers.ValidationError("Some product IDs are invalid.")

        # Validate stock for each product
        for item in data['products']:
            product = products.get(product_id=item['product_id'])
            if product.stock < item['quantity']:
                raise serializers.ValidationError(f"Product '{product.product_name}' is out of stock.")

        return data

    @transaction.atomic
    def create(self, validated_data):
        product_list = validated_data['products']
        user = self.context['request'].user
        customer, created = Customer.objects.get_or_create(user=user)

        # Get products and group them by vendor
        product_ids = [item['product_id'] for item in product_list]
        products = Product.objects.filter(product_id__in=product_ids).select_related('created_by')
        vendor_products = {}
        for item in product_list:
            product = products.get(product_id=item['product_id'])
            vendor = product.created_by
            if vendor not in vendor_products:
                vendor_products[vendor] = []
            vendor_products[vendor].append({'product': product, 'quantity': item['quantity']})

        created_orders = []
        order_id = Order.objects.all().aggregate(max_id=Max('order_id'))['max_id']
        order_product_id = OrderProduct.objects.all().aggregate(max_id=Max('order_product_id'))['max_id']
        for vendor, items in vendor_products.items():
            order_id += 1
            # Create an order for each vendor
            order = Order.objects.create(
                order_id=order_id,
                order_number=str(uuid4()),
                customer=customer,
                order_total=0,
            )

            total_price = 0
            for item in items:
                order_product_id += 1
                product = item['product']
                quantity = item['quantity']

                # Deduct stock and add product to the order
                if product.stock < quantity:
                    raise serializers.ValidationError(f"Sản phẩm '{product.product_name}' đã hết hàng.")
                product.stock -= quantity
                product.save()

                price = product.original_price
                OrderProduct.objects.create(
                    order_product_id = order_product_id,
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                total_price += price * quantity

            # Update order total
            order.order_total = total_price
            order.save()

            created_orders.append(order)

        return created_orders

