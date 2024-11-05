from django.urls import path
from apps.metabase.views import MetabaseDashboardView
urlpatterns = [
    path('api/vendor/dashboard', MetabaseDashboardView.as_view(), name='vendor-summary-dashboard')
]