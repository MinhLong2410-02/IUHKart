from django.contrib import admin
from apps.customers.models import Customer, User
# Register your models here.
admin.site.register(Customer)
admin.site.register(User)