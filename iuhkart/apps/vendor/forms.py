from apps.customers.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import ModelForm
from apps.product.models import Product

from .models import Vendor

class VendorSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=False, help_text='Full name of the vendor')
    phone = forms.CharField(max_length=20, required=False, help_text='Contact phone number')
    description = forms.CharField(widget=forms.Textarea, required=False, help_text='Short description about the vendor')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(VendorSignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vendor = True
        if commit:
            user.save()
            vendor = Vendor.objects.create(
                user=user,
                name=self.cleaned_data.get('name'),
                phone=self.cleaned_data.get('phone'),
                description=self.cleaned_data.get('description')
            )
            return vendor
        return user

class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ('product_name', 'category', 'original_price', 'product_description', 'stock',
                  'brand')
        labels = {
            'product_name': 'Title',
            'category': 'Category',
            'original_price': 'Price',
            'product_description': 'Description',
            'stock': 'In Stock',
            'brand': 'Size',
        }
