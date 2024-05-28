from rest_framework import serializers
from apps.review.models import Review
# create a serializer for read all reviews of a product
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['review_id', 'review_rating', 'review_content', 'review_date', 'customer']