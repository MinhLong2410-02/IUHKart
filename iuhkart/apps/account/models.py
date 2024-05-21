from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from apps.address.models import Address
from apps.account.manager import UserManager
from django.utils.translation import gettext_lazy as _
from apps.custom_storage import AzureCustomerStorage, AzureVendorStorage
# Create your models here.
class User(AbstractBaseUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, max_length=255)
    address = models.OneToOneField(Address, models.DO_NOTHING, blank=True, null=True)
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'user'

class Customer(models.Model):
    phone = models.CharField(max_length=17, blank=True, null=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', blank=True, null=True)
    fullname = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.SmallIntegerField()
    avatar_url = models.ImageField(storage=AzureCustomerStorage(), max_length=255, blank=True, null=True)
    class Meta:
        verbose_name_plural = "Customers"
        db_table = 'customer'
        

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo_url = models.ImageField(storage=AzureVendorStorage(), blank=True, null=True)
    class Meta:
        verbose_name_plural = "Vendors"
        db_table = 'vendor'