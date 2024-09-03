from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register_account(request):
    return render(request, 'register_account.html')
