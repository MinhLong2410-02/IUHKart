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

    class Meta:
        managed = False
        db_table = 'vendor'
    