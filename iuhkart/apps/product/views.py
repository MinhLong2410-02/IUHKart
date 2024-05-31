from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from apps.product.serializers import *
from apps.product.pagination import VendorProductResultsSetPagination
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiParameter

# Create your views here.

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='category_id',
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description='If category_id is None, all categories will be returned. Otherwise, only the category with the specified category_id will be returned.'
        )
    ]
)
class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny]
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()  
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset
@extend_schema(
    summary="Get all vendor's products.",
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
        OpenApiParameter(
            name='category_id',
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description='If category_id is None, all product will be returned.'
        )
    ],
)
class VendorProductListView(generics.ListAPIView):
    serializer_class = VendorProductSerializer
    pagination_class = VendorProductResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendor = self.request.user.vendor
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            return Product.objects.filter(created_by=vendor, category=category_id).select_related('created_by', 'category').prefetch_related('images')
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
        OpenApiParameter(
            name='category_id',
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description='If category_id is None, all product will be returned.'
        )
    ],
)
class CustomerProductListView(generics.ListAPIView):
    serializer_class = CustomerProductSerializer
    pagination_class = VendorProductResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all().select_related('created_by', 'category').prefetch_related('images')
    def get_queryset(self):
        queryset = super().get_queryset()  
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            return Product.objects.filter(category=category_id).select_related('created_by', 'category').prefetch_related('images')
        return queryset

class CustomerOneProductView(generics.RetrieveAPIView):
    serializer_class = CustomerSpecificProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Product.objects.select_related('created_by', 'category').prefetch_related('images')


class VendorProductCreateView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.vendor)

class VendorProductUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        exclude=True,
        methods=['PATCH']
    )
    def patch(self, request, *args, **kwargs):
        pass
    
    def get_queryset(self):
        return Product.objects.filter(created_by=self.request.user.vendor)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    def perform_update(self, serializer):
        serializer.save(partial=True)
class VendorProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BasicSerializer

    def get_queryset(self):
        return Product.objects.filter(created_by=self.request.user.vendor)

class ProductImageCreateView(generics.CreateAPIView):
    serializer_class = ProductImageCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(id=product_id, created_by=self.request.user.vendor)
        serializer.save(product=product)

class ProductImageUpdateView(generics.UpdateAPIView):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImageCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductImages.objects.filter(product_id=product_id, product__created_by=self.request.user.vendor)
    @extend_schema(
        exclude=True,
        methods=['PATCH']
    )
    def patch(self, request, *args, **kwargs):
        pass
class ProductImageDeleteView(generics.DestroyAPIView):
    queryset = ProductImages.objects.all()
    serializer_class = BasicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductImages.objects.filter(product_id=product_id, product__created_by=self.request.user.vendor)

class ProductImageBulkUpdateCreateView(GenericAPIView):
    serializer_class = ProductImageCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id, created_by=request.user.vendor)
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        product = Product.objects.get(id=product_id, created_by=request.user.vendor)
        images = ProductImages.objects.filter(product=product)
        serializer = self.get_serializer(images, data=request.data, many=True, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = Product.objects.get(id=product_id, created_by=request.user.vendor)
        image_ids = request.data.get('image_ids', [])
        ProductImages.objects.filter(product=product, id__in=image_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
