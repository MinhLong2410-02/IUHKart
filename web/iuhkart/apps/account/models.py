from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from apps.account.manager import UserManager
from django.utils.translation import gettext_lazy as _
from apps.custom_storage import AzureCustomerStorage, AzureVendorStorage
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
# Create your models here.
class User(AbstractBaseUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, max_length=255)
    address = models.OneToOneField('address.Address', models.DO_NOTHING, blank=True, null=True)
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

class Customer(models.Model):
    phone = models.CharField(max_length=17, blank=True, null=True)
    cart = models.OneToOneField('cart.Cart', on_delete=models.CASCADE, blank=True, null=True, db_column='cart_id')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', blank=True, null=True)
    fullname = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    age = models.SmallIntegerField()
    gender = models.CharField(max_length=10, default='male')
    avatar_url = models.ImageField(storage=AzureCustomerStorage(), max_length=255, blank=True, null=True)
    date_join = models.DateTimeField(default=timezone.now)
    recommend_products = ArrayField(models.IntegerField(), blank=True, default=list, size=20, db_column='recommend_product_ids')
    class Meta:
        verbose_name_plural = "Customers"
        db_table = 'customers'
        

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo_url = models.ImageField(storage=AzureVendorStorage(), blank=True, null=True)
    date_join = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Vendors"
        db_table = 'vendors'

class BankAccount(models.Model):
    bank_account_id = models.AutoField(primary_key=True, db_column='bank_account_id')
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, related_name='bank_account', db_column='vendor_id')
    bank_name = models.CharField(max_length=255, null=True)
    account_number = models.CharField(max_length=255, null=True) 
    account_holder_name = models.CharField(max_length=255, null=True)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'bank_accounts'