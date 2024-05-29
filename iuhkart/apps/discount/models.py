from django.db import models

# Create your models here.
class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    products = models.ManyToManyField('product.Product', through='ProductDiscount')
    date_created = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'discount'

    def __str__(self):
        return self.name

class ProductDiscount(models.Model):
    product_discount_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, db_column='product_id')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, db_column='discount_id')
    start_date = models.DateField()
    end_date = models.DateField()
    
    class Meta:
        db_table = 'product_discount'
        unique_together = (('product', 'discount'),)
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
        ]
        
    # def clean(self):
    #     if self.end_date < self.start_date:
    #         raise ValidationError('End date cannot be before start date.')

    def __str__(self):
        return f"{self.product} - {self.discount} ({self.start_date} to {self.end_date})"

class OrderProductDiscount(models.Model):
    order_product = models.ForeignKey('order.OrderProduct', on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'order_product_discount'
        unique_together = (('order_product', 'discount'),)
        
    def __str__(self):
        return f"{self.order_product} - {self.discount}"