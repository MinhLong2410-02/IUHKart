from rest_framework import serializers
from apps.address.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_id', 'province_id', 'address_detail']
        extra_kwargs = {
            'address_id': {'read_only': True},
        }

class UserAddressUpdateSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ['address']

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        if instance.address:
            address = instance.address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()
        else:
            address = Address.objects.create(**address_data)
            instance.address = address
        
        instance.save()
        return instance

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['province_id', 'province_name', 'province_name_en', 'type']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['district_id', 'province_id', 'district_name', 'district_name_en', 'type']

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ['ward_id', 'district_id', 'province_id', 'ward_name', 'ward_name_en', 'type']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_id', 'province_id', 'address_detail']
