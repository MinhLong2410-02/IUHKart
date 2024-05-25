from rest_framework import serializers
from apps.cart.models import Cart, Product, CartProduct

class CartProductSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product_id.product_name')
    product_image = serializers.ImageField(source='product_id.image')  # assuming you have an image field in Product model

    class Meta:
        model = CartProduct
        fields = ['cart_product_id', 'product_name', 'product_image', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(source='cartproduct_set', many=True)

    class Meta:
        model = Cart
        fields = ['cart_id', 'products', 'grand_total', 'items_total']

class UpdateCartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['quantity']
