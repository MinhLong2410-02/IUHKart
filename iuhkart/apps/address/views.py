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
        return self.request.user.address
    @extend_schema(
        exclude=True,
        methods=['GET', 'PATCH']
    )
    def patch(self, request, *args, **kwargs):
        pass
    