from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Vendor(models.Model):
    vendor_id = models.IntegerField(primary_key=True)
    address = models.ForeignKey('Address', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_by = models.OneToOneField(User, models.CASCADE, db_column='created_by', blank=True, null=True, related_name='vendor')
    class Meta:
        managed = False
        db_table = 'vendor'
        ordering = ['name']
    def __str__(self) -> str:
        return self.name
    
class Address(models.Model):
    address_id = models.IntegerField(primary_key=True)
    city_province = models.CharField(max_length=100, blank=True, null=True)
    address_detail = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address'
    