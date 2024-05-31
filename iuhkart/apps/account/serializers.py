from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.account.models import Customer, Vendor, BankAccount
from apps.cart.models import Cart
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import date

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'address')
        extra_kwargs = {
            'password': {'write_only': True},
            'address': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            is_customer=validated_data.get('is_customer', False),
            is_vendor=validated_data.get('is_vendor', False),
            address=validated_data.get('address')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomerDOBUpdateSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(required=True)

    class Meta:
        model = Customer
        fields = ('date_of_birth',)

    def validate_date_of_birth(self, value):
        if value >= date.today():
            raise serializers.ValidationError("The date of birth cannot be in the future.")
        return value

    def update(self, instance, validated_data):
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        
        today = date.today()
        instance.age = today.year - instance.date_of_birth.year - ((today.month, today.day) < (instance.date_of_birth.month, instance.date_of_birth.day))
        
        instance.save()
        return instance


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Customer
        fields = ('id', 'user', 'fullname', 'phone', 'date_of_birth')
    def isUserIsVendor(self, user):
        vendor = Vendor.objects.filter(user=user)
        return vendor.exists()
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        date_of_birth = validated_data.pop('date_of_birth', None)
        if date_of_birth:
            age = self.calculate_age(date_of_birth)
        else:
            age = None
        cart = Cart.objects.create()
        customer = Customer.objects.create(user=user, cart = cart, date_of_birth=date_of_birth, age=age, **validated_data)
        user.is_customer = True
        if not self.isUserIsVendor(user):
            user.save()
            
        return customer

    def calculate_age(self, birthdate):
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendor
        fields = ('id', 'user', 'name', 'phone', 'description')

    def isUserIsCustomer(self, user):
        customer = Customer.objects.filter(user=user)
        return customer.exists()
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        vendor = Vendor.objects.create(user=user, **validated_data)
        user.is_vendor = True
        if not self.isUserIsCustomer(user):
            user.save()
        return vendor

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        roles = []
        customer_id = None
        vendor_id = None
        
        # Check if the user has a customer profile
        if hasattr(self.user, 'customer'):
            roles.append('customer')
            customer_id = self.user.customer.id
        
        # Check if the user has a vendor profile
        if hasattr(self.user, 'vendor'):
            roles.append('vendor')
            vendor_id = self.user.vendor.id

        # Add roles and IDs to the token data
        data.update({
            'role': roles,
            'customer_id': customer_id,
            'vendor_id': vendor_id
        })

        return data

class CustomerAvatarUploadSerializer(serializers.ModelSerializer):
    avatar_url = serializers.ImageField()
    class Meta:
        model = Customer
        fields = ['avatar_url']

    def validate_avatar_url(self, value):
        if value.size > 1024 * 1024 * 5:
            raise serializers.ValidationError("Avatar size should not exceed 5MB.")
        return value

class VendorLogoUploadSerializer(serializers.ModelSerializer):
    logo_url = serializers.ImageField()
    class Meta:
        model = Vendor
        fields = ['logo_url']

    def validate_logo_url(self, value):
        if value.size > 1024 * 1024 * 5:
            raise serializers.ValidationError("Logo size should not exceed 5MB.")
        return value

class DetailedVendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendor
        fields = ('id', 'user', 'name', 'phone', 'description', 'logo_url', 'date_join')

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['bank_name', 'account_number', 'account_holder_name', 'branch_name']
        extra_kwargs = {
            'account_number': {'write_only': True}  # For security reasons, you might want to make the account number write-only
        }

    def validate_account_number(self, value):
        # Add validation for the account number if necessary, e.g., check format or encrypt
        return value