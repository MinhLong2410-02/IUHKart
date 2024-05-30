from django.db import models
from django.utils import timezone
# Create your models here.
class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey('account.Vendor', on_delete=models.CASCADE, db_column='vendor_id')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, db_column='product_id')
    name = models.CharField(max_length=100)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateField(default=timezone.now)
    start_date = models.DateField()
    end_date = models.DateField()
    in_use = models.BooleanField(default=True)
    class Meta:
        db_table = 'discount'
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
        ]

    def __str__(self):
        return self.name
class OrderProductDiscount(models.Model):
    order_product = models.ForeignKey('order.OrderProduct', on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'order_product_discount'
        unique_together = (('order_product', 'discount'),)
        
    def __str__(self):
        return f"{self.order_product} - {self.discount}"