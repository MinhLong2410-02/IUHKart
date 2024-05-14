from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import ModelForm

from .models import Customer, User

class CustomerSignUpForm(UserCreationForm):
    address = forms.CharField(widget=forms.Textarea)
    full_name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=17)

    def __init__(self, *args, **kwargs):
        super(CustomerSignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ["password1", "password2"]:
            self.fields[fieldname].help_text = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(
            user=user,
            fullname=self.cleaned_data.get('full_name'),
            address=self.cleaned_data.get('address'),
            phone=self.cleaned_data.get('phone')
        )
        customer.save()
        return customer

class CustomerUpdateForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('fullname', 'avatar_url', 'phone', 'date_of_birth')

    def save(self, commit=True):
        customer = super().save(commit=False)
        if customer.user:
            customer.user.email = self.cleaned_data.get('email', customer.user.email)
            customer.user.save()
        if commit:
            customer.save()
        return customer
