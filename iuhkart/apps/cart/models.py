from django.db import models

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    items_total = models.PositiveIntegerField(default=0)
    class Meta:
        db_table = 'carts'
        verbose_name_plural = 'Carts'
        ordering = ['-cart_id']

class CartProduct(models.Model):
    cart_product_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products', db_column='cart_id')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, db_column='product_id')
    quantity = models.PositiveIntegerField()
    class Meta:
        db_table = 'cart_products'
        ordering = ['-cart_id']