from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html')

def listar_view(request):
    
    return render(request, 'listar.html')

def agregar_view(request):
    return render(request, 'agregar.html')

def admin_view(request):
    return render(request, 'admin.html')

def login_view(request):
    return render(request, 'login.html')

