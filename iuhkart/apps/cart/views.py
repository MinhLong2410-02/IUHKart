from rest_framework import status, generics, viewsets, permissions
from rest_framework.response import Response
from apps.cart.models import Cart, CartProduct
from apps.cart.serializers import CartSerializer, CartProductSerializer, UpdateCartProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    def create(self, request, *args, **kwargs):
        # Implement logic to create a cart
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Implement logic to delete a product from the cart or the whole cart
        pk = kwargs.get('pk')
        cart_product = CartProduct.objects.filter(cart_product_id=pk)
        if cart_product.exists():
            cart_product.delete()
            return Response({'status': 'product removed'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        # Update product quantity in the cart
        cart_product_id = request.data.get('cart_product_id')
        quantity = request.data.get('quantity')
        cart_product = CartProduct.objects.get(pk=cart_product_id)
        serializer = UpdateCartProductSerializer(cart_product, data={'quantity': quantity}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartDetailsView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        customer = request.user.customer
        try:
            cart = Cart.objects.get(customer_id=customer)
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)