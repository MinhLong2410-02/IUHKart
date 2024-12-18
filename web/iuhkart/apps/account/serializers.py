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
    date_of_birth = serializers.DateTimeField(required=False, allow_null=True)

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
        product_ids = Product.objects.order_by('-ratings').values_list('product_id', flat=True)[:20]
        customer.recommend_product_ids = list(product_ids)
        customer.save()
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
        fields = ['bank_name', 'account_number', 'account_holder_name', 'money']
        extra_kwargs = {
            'account_number': {'write_only': True},
            'money': {'read_only': True},  # Prevent users from modifying balance directly
        }

    def validate_account_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Account number must be numeric.")
        if len(value) < 8:
            raise serializers.ValidationError("Account number must be at least 8 digits long.")
        return value

class UpdateMoneySerializer(serializers.Serializer):
    money = serializers.IntegerField(min_value=0)

    def validate(self, attrs):
        money = attrs.get("money")
        if money is None:
            raise serializers.ValidationError("The 'money' field is required.")
        return attrs