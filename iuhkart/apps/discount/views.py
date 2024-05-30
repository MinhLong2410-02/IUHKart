from django.shortcuts import render
from apps.discount.serializers import DiscountSerializer
from rest_framework import generics, permissions
from apps.discount.models import Discount
from apps.product.models import Product
from drf_spectacular.utils import extend_schema
from datetime import date 

from django.http import Http404
# Create your views here.
class CreateDiscountView(generics.CreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Ensure that the vendor creating the discount is the logged-in user and product exists.
        Also, automatically set 'in_use' if start_date is today or in the past.
        """

        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(pk=product_id)

        # Check if the vendor owns the product
        if self.request.user.vendor != product.created_by:
            raise permissions.PermissionDenied("You do not own this product.")

        # Automatically set 'in_use' based on the start date
        start_date = serializer.validated_data['start_date']
        in_use = start_date <= date.today()

        serializer.save(vendor=self.request.user.vendor, product=product, in_use=in_use)
    
class DiscountCreateUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Assuming the vendor is the logged-in user and product_id is passed in the request
        serializer.save(vendor=self.request.user.vendor)

    def get_object(self):
        product_id = self.kwargs.get('product_id')
        discount, created = Discount.objects.get_or_create(product_id=product_id, defaults={'vendor': self.request.user.vendor})
        return discount
    @extend_schema(
        exclude=True,
        methods=['GET', 'PATCH']
    )
    def patch(self, request, *args, **kwargs):
        pass
class DiscountDeleteView(generics.DestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        product_id = self.kwargs.get('product_id')
        try:
            return Discount.objects.get(product_id=product_id, vendor=self.request.user.vendor)
        except Discount.DoesNotExist:
            raise Http404