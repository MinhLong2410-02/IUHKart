from apps.customers.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import ModelForm
from apps.product.models import Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import Vendor
from django.contrib.auth import get_user_model
User = get_user_model()

class VendorSignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, help_text='Enter a valid email address')
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Vendor
        fields = ['name', 'phone', 'description']

    def __init__(self, *args, **kwargs):
        super(VendorSignUpForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['phone'].required = False
        self.fields['description'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Password must match.")
        
        return cleaned_data

    def save(self, commit=True):
        user_data = {
            'email': self.cleaned_data['email'],
            'password': self.cleaned_data['password'],
        }
        user = User.objects.create_user(**user_data)
        user.is_vendor = True
        user.set_password(self.cleaned_data['password'])  # Ensures the password is hashed
        user.save()

        vendor = super(VendorSignUpForm, self).save(commit=False)
        vendor.user = user
        if commit:
            vendor.save()
        return vendor

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
