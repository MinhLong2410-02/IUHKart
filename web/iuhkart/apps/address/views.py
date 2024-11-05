from rest_framework import generics, permissions
from apps.address.models import Province, District, Ward, Address
from apps.address.serializers import ProvinceSerializer, DistrictSerializer, WardSerializer, AddressSerializer
from drf_spectacular.utils import extend_schema

class ProvinceListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class DistrictListView(generics.ListAPIView):
    serializer_class = DistrictSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        province_id = self.kwargs.get('province_id')
        return District.objects.filter(province_id=province_id)

class WardListView(generics.ListAPIView):
    serializer_class = WardSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        district_id = self.kwargs.get('district_id')
        return Ward.objects.filter(district_id=district_id)

class AddressUpdateView(generics.UpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Check if the user has an address
        address = self.request.user.address
        if not address:
            # Create a new Address record if none exists
            address = Address.objects.create()
            # Link the new Address to the user's address field
            self.request.user.address = address
            self.request.user.save()  # Save the user to persist the change
        return address
    
    @extend_schema(
        exclude=True,
        methods=['GET', 'PATCH']
    )
    def patch(self, request, *args, **kwargs):
        pass
    