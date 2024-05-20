from rest_framework import generics, permissions
from apps.address.serializers import *

class ProvinceListView(generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class DistrictListView(generics.ListAPIView):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        province_id = self.kwargs.get('province_id')
        return District.objects.filter(province_id=province_id)

class WardListView(generics.ListAPIView):
    serializer_class = WardSerializer

    def get_queryset(self):
        province_id = self.kwargs.get('province_id')
        return Ward.objects.filter(province_id=province_id)

class AddressUpdateView(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.address
