from rest_framework import serializers
from apps.discount.models import Discount
from datetime import date

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['discount_id', 'name', 'discount_percent']
        read_only_fields = ['date_created']

    def validate(self, data):
        """
        Ensure the end date is after the start date and adjust 'in_use' based on start date.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after the start date.")
        
        # Automatically set 'in_use' to True if the start date is today or in the past
        if data['start_date'] <= date.today():
            data['in_use'] = True
        else:
            data['in_use'] = False
        
        return data

    def create(self, validated_data):
        """
        Create a new Discount instance.
        """
        return Discount.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Discount instance.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.discount_percent = validated_data.get('discount_percent', instance.discount_percent)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        
        # Update 'in_use' based on the start date
        if validated_data.get('start_date', instance.start_date) <= date.today():
            instance.in_use = True
        else:
            instance.in_use = False

        instance.save()
        return instance

