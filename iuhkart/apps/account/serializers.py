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
    email = serializers.EmailField(write_only=True)  # Capture email directly since there's no user link
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Customer
        fields = ('id', 'email', 'fullname', 'phone', 'date_of_birth')

    def create(self, validated_data):
        email = validated_data.pop('email')
        user, is_exist = User.objects.get_or_create(email=email)
        user.set_password(validated_data.get('password', 'defaultpassword'))  # You can adjust this logic
        user.save()

        date_of_birth = validated_data.pop('date_of_birth', None)
        cart = Cart.objects.create()
        customer = Customer.objects.create(cart=cart, date_of_birth=date_of_birth, **validated_data)
        customer.user = user
        product_ids = Product.objects.order_by('-ratings').values_list('product_id', flat=True)[:20]
        customer.recommend_product_ids = list(product_ids)
        customer.save()
        
        return customer


class VendorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)  # Capture email separately

    class Meta:
        model = Vendor
        fields = ('id', 'email', 'name', 'phone', 'description')

    def create(self, validated_data):
        email = validated_data.pop('email')
        user, is_exist = User.objects.get_or_create(email=email)
        
        user.set_password(validated_data.get('password', 'defaultpassword'))
        user.save()
        vendor = Vendor.objects.create(**validated_data)
        vendor.user = user
        vendor.save()
        return vendor


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        roles = list(self.user.roles.values_list('name', flat=True))

        # Handling the fact that User does not directly relate to Customer and Vendor
        customer = Customer.objects.filter(fullname=self.user.get_full_name()).first()
        vendor = Vendor.objects.filter(name=self.user.get_full_name()).first()

        customer_id = customer.id if customer else None
        vendor_id = vendor.id if vendor else None

        data.update({
            'roles': roles,
            'customer_id': customer_id,
            'vendor_id': vendor_id
        })
        return data

class CustomerTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Check if the user is linked to a customer
        try:
            customer = Customer.objects.get(user=self.user)
            data.update({
                'roles': ['customer'],
                'customer_id': customer.id,
                'fullname': customer.fullname
            })
        except Customer.DoesNotExist:
            raise serializers.ValidationError("No customer account associated with this user.")
        
        return data


class VendorTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Check if the user is linked to a vendor
        try:
            vendor = Vendor.objects.get(user=self.user)
            data.update({
                'roles': ['vendor'],
                'vendor_id': vendor.id,
                'vendor_name': vendor.name
            })
        except Vendor.DoesNotExist:
            raise serializers.ValidationError("No vendor account associated with this user.")
        
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
    class Meta:
        model = Vendor
        fields = ('id', 'name', 'phone', 'description', 'logo_url', 'date_join')


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['bank_name', 'account_number', 'account_holder_name', 'branch_name']
        extra_kwargs = {
            'account_number': {'write_only': True}
        }

    def validate_account_number(self, value):
        return value
