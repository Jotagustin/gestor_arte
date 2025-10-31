from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def listar(request):
    return render(request, 'listar.html')

def agregar(request):
    return render(request, 'agregar.html')

def admin(request):
    return render(request, 'admin.html')

def login(request):
    return render(request, 'login.html')
