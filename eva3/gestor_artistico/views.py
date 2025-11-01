from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index_view(request):
    return render(request, 'index.html')

@login_required(login_url='login_view')
def listar_view(request):
    return render(request, 'listar.html')

@login_required(login_url='login_view')
def agregar_view(request):
    return render(request, 'agregar.html')

@login_required(login_url='login_view')
def admin_view(request):
    return render(request, 'admin.html')


@login_required(login_url='login_view')
def logout_view(request):
    """Cerrar sesión y redirigir al login."""
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login_view')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.POST.get('next') or 'listar'
                return redirect(next_url)
            else:
                messages.error(request, "Cuenta desactivada.")
        else:
            messages.error(request, "Credenciales incorrectas.")

    return render(request, 'login.html')

