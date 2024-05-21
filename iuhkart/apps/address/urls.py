from django.urls import path
from apps.address.views import *

urlpatterns = [
    path('api/provinces/', ProvinceListView.as_view(), name='province-list'),
    path('api/provinces/<int:province_id>/districts/', DistrictListView.as_view(), name='district-list'),
    path('api/districts/<int:district_id>/wards/', WardListView.as_view(), name='ward-list'),
    path('api/user/update_address/', AddressUpdateView.as_view(), name='user-update-address'),
]