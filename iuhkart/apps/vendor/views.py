from django.shortcuts import render

# Create your views here.
# create a simple view function that will render HELLO WORLD
def home(request):
    return "HELLO WORLD"