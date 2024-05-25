from django.db import models
from apps.product.models import Product, Customer

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer_id = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product_id = models.ManyToManyField(Product, through='CartProduct')
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    items_total = models.PositiveIntegerField()
    class Meta:
        db_table = 'cart'
        verbose_name_plural = 'Carts'
        ordering = ['-cart_id']

class CartProduct(models.Model):
    cart_product_id = models.AutoField(primary_key=True)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()