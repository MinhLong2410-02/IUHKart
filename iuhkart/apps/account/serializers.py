from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.account.models import Customer, Vendor, BankAccount
from apps.product.models import Product
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

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        date_of_birth = validated_data.pop('date_of_birth', None)
        cart = Cart.objects.create()
        customer = Customer.objects.create(user=user, cart=cart, date_of_birth=date_of_birth, **validated_data)
        product_ids = Product.objects.order_by('-ratings').values_list('id', flat=True)[:20]
        customer.recommend_product_ids = list(product_ids)
        customer.save()
        return customer

class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendor
        fields = ('id', 'user', 'name', 'phone', 'description')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        vendor = Vendor.objects.create(user=user, **validated_data)
        return vendor

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        roles = list(self.user.roles.values_list('name', flat=True))
        customer_id = getattr(self.user.customer, 'id', None)
        vendor_id = getattr(self.user.vendor, 'id', None)
        data.update({
            'roles': roles,
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
            'account_number': {'write_only': True}
        }

    def validate_account_number(self, value):
        return value
