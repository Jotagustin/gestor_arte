from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Artista, Proyecto, Colaboracion, PerfilUsuario

@login_required(login_url='login_view')
def index_view(request):
    """Dashboard / landing page for logged users.

    Shows user's own projects and other projects and provides a modal to create new projects.
    """
    def get_or_create_artista_for_user(user):
        nombre = user.username
        artista, _ = Artista.objects.get_or_create(nombre=nombre)
        return artista

    user = request.user
    artista = get_or_create_artista_for_user(user)

    my_projects = Proyecto.objects.filter(artista=artista)
    other_projects = Proyecto.objects.exclude(artista=artista)

    context = {
        'artista': artista,
        'my_projects': my_projects,
        'other_projects': other_projects,
    }
    return render(request, 'index.html', context)

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
                next_url = request.POST.get('next') or 'index_view'
                return redirect(next_url)
            else:
                messages.error(request, "Cuenta desactivada.")
        else:
            messages.error(request, "Credenciales incorrectas.")

    return render(request, 'login.html')


@login_required(login_url='login_view')
def crear_proyecto(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        if not titulo:
            messages.error(request, 'El título es obligatorio.')
            return redirect('listar')

        nombre = request.user.username
        artista = Artista.objects.get_or_create(nombre=nombre)[0]
        Proyecto.objects.create(artista=artista, titulo=titulo, descripcion=descripcion or '')
        messages.success(request, 'Proyecto creado correctamente.')
    return redirect('listar')


@login_required(login_url='login_view')
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    artista = Artista.objects.get_or_create(nombre=request.user.username)[0]
    if proyecto.artista != artista:
        messages.error(request, 'No tienes permiso para eliminar este proyecto.')
        return redirect('listar')
    proyecto.delete()
    messages.success(request, 'Proyecto eliminado.')
    return redirect('listar')


@login_required(login_url='login_view')
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    artista = Artista.objects.get_or_create(nombre=request.user.username)[0]
    if proyecto.artista != artista:
        messages.error(request, 'No tienes permiso para editar este proyecto.')
        return redirect('listar')
    if request.method == 'POST':
        proyecto.titulo = request.POST.get('titulo') or proyecto.titulo
        proyecto.descripcion = request.POST.get('descripcion') or proyecto.descripcion
        proyecto.save()
        messages.success(request, 'Proyecto actualizado.')
        return redirect('listar')
    return render(request, 'agregar.html', {'proyecto': proyecto})


@login_required(login_url='login_view')
def agregar_colaborador(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    if request.method == 'POST':
        nombre_artista = request.POST.get('nombre_artista')
        if not nombre_artista:
            messages.error(request, 'Debe indicar el nombre del artista a añadir.')
            return redirect('listar')
        artista_obj, _ = Artista.objects.get_or_create(nombre=nombre_artista)
        Colaboracion.objects.get_or_create(proyecto=proyecto, artista=artista_obj)
        messages.success(request, f'Artista {nombre_artista} agregado como colaborador.')
    return redirect('listar')

