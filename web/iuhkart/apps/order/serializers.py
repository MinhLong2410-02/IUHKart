from rest_framework import serializers
from apps.account.models import Customer, BankAccount, Vendor
from apps.order.models import Order, OrderProduct, Transaction
from apps.product.models import Product
from apps.discount.models import Discount, OrderProductDiscount
from django.db import transaction
from django.db.models import Max
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

class ProcessTransactionSerializer(serializers.Serializer):
    order_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="A list of order IDs to process transactions for."
    )

    def validate(self, data):
        user = self.context['request'].user
        orders = Order.objects.filter(order_id__in=data['order_ids'], customer=user.customer, order_status='pending')
        
        if not orders.exists():
            raise serializers.ValidationError("No valid pending orders found for the given IDs.")
        
        total_amount = sum(order.order_total for order in orders)
        if user.bank_account.money < total_amount:
            raise serializers.ValidationError("Tài khoản bạn không đủ tiền.")

        data['orders'] = orders
        return data

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        orders = validated_data['orders']

        # Retrieve the largest transaction_id
        transaction_id = Transaction.objects.all().aggregate(Max('transaction_id'))['transaction_id__max'] or 0
        transactions = []

        for order in orders:
            vendors = {}
            order_total = 0

            # Group money by vendor
            for order_product in order.orderproduct_set.all():
                transaction_id += 1
                vendor = order_product.product.created_by
                price = order_product.price * order_product.quantity

                if vendor not in vendors:
                    vendors[vendor] = 0
                vendors[vendor] += price
                order_total += price

            # Deduct money from the user's bank account
            user_bank_account = BankAccount.objects.select_for_update().get(user_id=user.pk)
            user_bank_account.money -= order_total
            user_bank_account.save()

            # Distribute money to vendors' bank accounts
            for vendor, amount in vendors.items():
                vendor_bank_account = BankAccount.objects.select_for_update().get(user_id=vendor.user.pk)
                vendor_bank_account.money += amount
                vendor_bank_account.save()

            # Create a transaction
            transaction = Transaction.objects.create(
                transaction_id=transaction_id,
                order=order,
                customer=user.customer,
                total_money=order_total,
                status='completed'
            )
            transactions.append(transaction)

            # Update order status
            order.order_status = 'processing'
            order.save()

        return transactions