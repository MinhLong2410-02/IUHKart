from django.shortcuts import render
from apps.review.serializers import ReviewSerializer, Review
from rest_framework import generics

# Create your views here.

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product=product_id)