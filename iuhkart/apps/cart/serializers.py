from rest_framework import serializers
from apps.cart.models import Cart, CartProduct
from apps.product.models import Product, ProductImages
from django.db.models import Sum, F
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image_url']

class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'original_price', 'main_image']

    def get_main_image(self, obj):
        main_image = ProductImages.objects.filter(product_id = obj.product_id).first()
        if main_image:
            return ProductImageSerializer(main_image).data
        return None 
    
class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  
    class Meta:
        model = CartProduct
        fields = ['cart_product_id', 'product', 'quantity']
class AddCartProductSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(write_only=True)  

    class Meta:
        model = CartProduct
        fields = ['cart_product_id', 'product', 'quantity']

    def create(self, validated_data):
        product_id = validated_data['product']
        quantity = validated_data.get('quantity', 1) 
        product = Product.objects.get(pk=product_id) 

        # Retrieve the cart from the user (context passed in view)
        cart = self.context['request'].user.customer.cart
        stock = product.stock
        if quantity > stock:
            quantity = stock
        
        
        # Check if the product is already in the cart
        cart_product, created = CartProduct.objects.update_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}  # This updates the quantity if the row exists
        )
        if created:
            cart_product.quantity = quantity
            cart_product.save()
        cart_product = CartProduct.objects.filter(cart=cart, product=product).first()

        cart.items_total += quantity
        cart.grand_total += product.original_price * quantity
        cart.save()

        return cart_product

class GetCartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(source='cart_products', many=True)  # Use the correct related_name

    class Meta:
        model = Cart
        fields = ['cart_id', 'grand_total', 'items_total', 'products']

class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(source='cart_products', many=True)  # Adjust source if related_name is set

    class Meta:
        model = Cart
        fields = ['cart_id', 'grand_total', 'items_total', 'products']


class UpdateCartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['quantity']

    def validate_quantity(self, value):
        # Check if the requested quantity is available in the product's stock
        product = self.instance.product
        if value > product.stock:
            raise serializers.ValidationError("Insufficient stock available.")
        return value

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()

        # Update cart totals
        cart = instance.cart
        cart.items_total = CartProduct.objects.filter(cart=cart).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        cart.grand_total = CartProduct.objects.filter(cart=cart).aggregate(total_price=Sum(F('product__original_price') * F('quantity')))['total_price']
        cart.save()

        return instance