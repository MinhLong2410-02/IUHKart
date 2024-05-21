from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.account.models import Customer, Vendor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import date

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'is_customer', 'is_vendor', 'address')
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

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'user', 'fullname', 'phone', 'date_of_birth', 'avatar_url')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        
        date_of_birth = validated_data.pop('date_of_birth')
        age = self.calculate_age(date_of_birth)
        
        customer = Customer.objects.create(user=user, date_of_birth=date_of_birth, age=age, **validated_data)
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

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        vendor = Vendor.objects.create(user=user, **validated_data)
        return vendor

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = 'customer' if self.user.is_customer else 'vendor' if self.user.is_vendor else 'unknown'
        return data
