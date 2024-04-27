from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from apps.address.models import Address
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, **extra_fields)
        user.is_superuser = False
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email= self.normalize_email(email),
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', blank=True, null=True)
    fullname = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.SmallIntegerField()
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        verbose_name_plural = "Customers"
        db_table = 'customer'

