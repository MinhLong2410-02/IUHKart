from django.db import models
from autoslug import AutoSlugField
from apps.account.models import Vendor, Customer
# Create your models here.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    slug = AutoSlugField(max_length=100, populate_from='category_name')
    category_img_url = models.URLField(max_length=100)
    def __str__(self):
        return f"{self.category_id} - {self.category_name} - {self.category_img_url}"
    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'
        ordering = ['-category_id']

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)

    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    brand = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255, populate_from='product_name')
    product_description = models.TextField()
    
    created_by = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(Customer, related_name="customer", on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.product_id} - {self.product_name} - {self.original_price} - {self.stock} - {self.brand} - {self.created_by}"
    
    class Meta:
        db_table = 'product'
        verbose_name_plural = 'Products'
        ordering = ['-product_id']

class ProductImages(models.Model):
    product_image_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=255)
    is_main = models.BooleanField(default=False)