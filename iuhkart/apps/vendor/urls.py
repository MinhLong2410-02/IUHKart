# create a new file urls.py in vendor app and add the following code
# """
# URL configuration for vendor app.
# """
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
]