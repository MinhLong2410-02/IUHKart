from django.db import models
from django.utils import timezone
# Create your models here.
class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    # vendor = models.ForeignKey('account.Vendor', on_delete=models.CASCADE, db_column='vendor_id')
    # product = models.ForeignKey('product.Product', on_delete=models.CASCADE, db_column='product_id')
    # date_created = models.DateField(default=timezone.now)
    # start_date = models.DateField()
    # end_date = models.DateField()
    # in_use = models.BooleanField(default=True)
    class Meta:
        db_table = 'discounts'
        # indexes = [
        #     models.Index(fields=['start_date']),
        #     models.Index(fields=['end_date']),
        # ]

    def __str__(self):
        return self.name

# product_discount_id,product_id,discount_id,start_date,end_date
class OrderProductDiscount(models.Model):
    product_discount_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, db_column='product_id')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, db_column='discount_id')
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:
        db_table = 'order_product_discounts'
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
        ]

    def __str__(self):
        return f"{self.order_product} - {self.discount}"
        
