from rest_framework import serializers
from apps.review.models import Review
# create a serializer for read all reviews of a product
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['review_id', 'review', 'rating', 'customer', 'created_at']