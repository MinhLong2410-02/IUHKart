from django.urls import path
from apps.review.views import *
urlpatterns = [
    path('api/get-reviews/<int:product_id>/', ReviewList.as_view(), name='review-list'),
]