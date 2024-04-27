from django.db import models
from autoslug import AutoSlugField
from apps.vendor.models import Vendor
from apps.customers.models import Customer
# Create your models here.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    slug = AutoSlugField(max_length=100, populate_from='category_name')
    category_img_url = models.URLField(max_length=100)

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    brand = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255, populate_from='product_name')
    product_description = models.TextField()
    
    created_by = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="customer", on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'product'
        verbose_name_plural = 'Products'
        ordering = ['-product_id']