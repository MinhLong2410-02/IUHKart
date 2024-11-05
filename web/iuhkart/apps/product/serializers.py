from rest_framework import serializers
from apps.product.models import Product, ProductImages, Category
from drf_spectacular.utils import extend_schema_field

class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=False)

    class Meta:
        model = Category
        fields = ['category_id', 'category_name', 'category_img_url']
class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField()

    class Meta:
        model = ProductImages
        fields = ['product_image_id', 'image_url', 'is_main']
class ProductImageCreateUpdateSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField()

    class Meta:
        model = ProductImages
        fields = ['image_url']
class VendorProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'product_description', 'original_price', 'stock', 'brand', 'slug', 'created_by', 'category', 'images', 'ratings']

class CustomerProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'product_description', 'original_price', 'stock', 'brand', 'slug', 'created_by', 'category', 'images', 'ratings']
        
    @extend_schema_field(ProductImageSerializer(allow_null=True))
    def get_images(self, obj):
        main_image = ProductImages.objects.filter(product_id = obj.product_id).first()
        if main_image:
            return ProductImageSerializer(main_image).data
        return None
class CustomerSpecificProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'product_description', 'original_price', 'stock', 'brand', 'slug', 'created_by', 'category', 'images', 'ratings']
        
    @extend_schema_field(ProductImageSerializer(allow_null=True))
    def get_images(self, obj):
        images = ProductImages.objects.filter(product_id = obj.product_id)
        if images:
            return ProductImageSerializer(images, many=True).data
        return None

class ProductCreateSerializer(serializers.ModelSerializer):
    # images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['product_name', 'product_description', 'original_price', 'stock', 'brand', 'category']

    def create(self, validated_data):
        # images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        # for image_data in images_data:
        #     ProductImages.objects.create(product=product, **image_data)
        return product

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'product_description', 'original_price', 'stock', 'brand', 'slug', 'created_by', 'category', 'images', 'ratings']

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image_url']

class BasicSerializer(serializers.Serializer):
    pass