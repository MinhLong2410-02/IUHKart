from rest_framework import serializers
from apps.address.models import Province, District, Ward, Address
from django.contrib.auth import get_user_model

User = get_user_model()

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
    province_id = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all(), source='province')
    district_id = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), source='district')
    ward_id = serializers.PrimaryKeyRelatedField(queryset=Ward.objects.all(), source='ward')

    class Meta:
        model = Address
        fields = ['address_id', 'province_id', 'district_id', 'ward_id', 'address_detail']
        extra_kwargs = {
            'address_id': {'read_only': True},
        }

    def update(self, instance, validated_data):
        instance.province = validated_data.get('province', instance.province)
        instance.district = validated_data.get('district', instance.district)
        instance.ward = validated_data.get('ward', instance.ward)
        instance.address_detail = validated_data.get('address_detail', instance.address_detail)
        instance.save()
        return instance

class UserAddressUpdateSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ['address']

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address_serializer = self.fields['address']
        address_instance = instance.address

        if address_instance:
            address_serializer.update(address_instance, address_data)
        else:
            address_instance = address_serializer.create(address_data)
            instance.address = address_instance

        instance.save()
        return instance
