from rest_framework import serializers
from apps.product.models import Product, ProductImages

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image_url']

class VendorProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'product_description', 'original_price', 'stock', 'brand', 'slug', 'created_by', 'category', 'images']

class CustomerProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'product_description', 'original_price', 'stock', 'brand', 'slug', 'created_by', 'category', 'images']
        
    def get_images(self, obj):
        # Return a random image that belongs to the product with is_main=True
        image = obj.images.filter(is_main=True).first()
        if image:
            return ProductImageSerializer(image).data
        return None