from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, this is the home page of the challenges app.")
from django.shortcuts import render

# Create your views here.
