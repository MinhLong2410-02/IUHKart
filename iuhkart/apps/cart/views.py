from rest_framework import status, generics, permissions
from rest_framework.response import Response
from apps.cart.models import Cart, CartProduct
from apps.account.models import Customer
from apps.cart.serializers import *
from django.db.models import Sum, F
from drf_spectacular.utils import extend_schema


class ProductAddToCartView(generics.CreateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = AddCartProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Fetch the updated cart data
        cart = request.user.customer.cart
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
class ProductDeleteFromCartView(generics.DestroyAPIView):
    queryset = CartProduct.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer  

    def delete(self, request, product_id):
        cart = request.user.customer.cart
        try:
            cart_product = CartProduct.objects.get(cart_id=cart, product_id=product_id)  # Find the CartProduct entry
            cart_product.delete()
            cart.items_total = CartProduct.objects.filter(cart=cart).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            cart.grand_total = CartProduct.objects.filter(cart=cart).aggregate(total_price=Sum(F('product__original_price') * F('quantity')))['total_price'] or 0.00
            cart.save()

            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CartProduct.DoesNotExist:
            return Response({'error': 'Product not found in cart'}, status=status.HTTP_404_NOT_FOUND)
class ProductQuantityUpdateView(generics.UpdateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = UpdateCartProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Get the CartProduct based on the product_id and the user's cart
        product_id = self.kwargs.get('product_id')
        user = self.request.user
        cart = user.customer.cart  # Assuming a direct relation like user.customer.cart exists
        return CartProduct.objects.get(cart=cart, product=product_id)
    
    @extend_schema(
        exclude=True,
        methods=['PATCH']
    )
    def patch(self, request, *args, **kwargs):
        pass

class CartDetailView(generics.RetrieveAPIView):
    serializer_class = GetCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        customer = Customer.objects.get(user=self.request.user)
        try:
            return customer.cart 
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)