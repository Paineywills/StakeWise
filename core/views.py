from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def login_view(request):
    return render(request, 'core/login.html')

def register_view(request):
    return render(request, 'core/register.html')