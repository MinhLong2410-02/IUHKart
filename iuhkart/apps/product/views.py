from django.shortcuts import render
from rest_framework import generics, permissions
from apps.product.serializers import *
from apps.product.pagination import VendorProductResultsSetPagination
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiParameter  # Add this import statement
# Create your views here.
@extend_schema(
    summary="Get current vendor's products list.",
    description="This endpoint allows the authenticated vendor to retrieve a paginated list of their products.",
    parameters=[
        OpenApiParameter(
            name='page',
            type=int,
            location=OpenApiParameter.QUERY,
            description='The page number.',
        ),
        OpenApiParameter(
            name='page_size',
            type=int,
            location=OpenApiParameter.QUERY,
            description='Number of products per page. Default is 10.',
        ),
    ],
)
class VendorProductListView(generics.ListAPIView):
    serializer_class = VendorProductSerializer
    pagination_class = VendorProductResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        vendor = self.request.user.vendor
        return Product.objects.filter(created_by=vendor).select_related('created_by', 'category').prefetch_related('images')

@extend_schema(
    summary="Get all products for customer.",
    description="This endpoint allows the authenticated customer to retrieve a paginated list of random products.",
    parameters=[
        OpenApiParameter(
            name='page',
            type=int,
            location=OpenApiParameter.QUERY,
            description='The page number.',
        ),
        OpenApiParameter(
            name='page_size',
            type=int,
            location=OpenApiParameter.QUERY,
            description='Number of products per page. Default is 10.',
        ),
    ],
)
class CustomerProductListView(generics.ListAPIView):
    serializer_class = CustomerProductSerializer
    pagination_class = VendorProductResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all().select_related('created_by', 'category').prefetch_related('images')