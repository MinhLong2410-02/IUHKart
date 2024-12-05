from django.db import models
from datetime import timedelta
from django.utils.timezone import now

def default_shipping_date():
    return now() + timedelta(days=3)

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=50, unique=True, db_index=True)
    shipping_date = models.DateTimeField(default=default_shipping_date)
    order_date = models.DateTimeField(default=now)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='pending', db_index=True)
    order_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    customer = models.ForeignKey('account.Customer', on_delete=models.CASCADE, db_column='customer_id')
    address = models.ForeignKey('address.Address', on_delete=models.CASCADE, db_column='address_id', null=True, blank=True)

    class Meta:
        ordering = ['-order_date']
        db_table = 'orders'

    def __str__(self):
        return self.order_number

class OrderProduct(models.Model):
    order_product_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='order_id')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, db_column='product_id')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'order_products'
        ordering = ['-order_id']
        # unique_together = (('order', 'product'),)

class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    transaction_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    transation_date = models.DateTimeField(default=now)
    total_money = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS_CHOICES, default='pending')
    customer = models.ForeignKey('account.Customer', on_delete=models.CASCADE, db_column='customer_id')
    
    class Meta:
        ordering = ['-transation_date']
        db_table = 'transactions'

    def __str__(self):
        return f"{self.payment_id} - {self.order.order_number}"