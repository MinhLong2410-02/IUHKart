from rest_framework import serializers
from apps.review.models import Review
# create a serializer for read all reviews of a product
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['review_id', 'review_rating', 'review_content', 'review_date', 'customer_id']

class CustomerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['review_id', 'product_id', 'review_rating', 'review_date', 'review_content']
        read_only_fields = ['review_date']  # Auto-set fields should not be editable

    def create(self, validated_data):
        # Create the Review instance
        return Review.objects.create(**validated_data)