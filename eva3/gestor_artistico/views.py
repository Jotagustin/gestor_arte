from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Artista, Proyecto, Colaboracion, PerfilUsuario, Historial


@login_required(login_url='login_view')
def index_view(request):
    def get_or_create_artista_for_user(user):
        nombre = user.username
        artista, _ = Artista.objects.get_or_create(nombre=nombre)
        return artista

    user = request.user
    artista = get_or_create_artista_for_user(user)
    perfil = PerfilUsuario.objects.get(user=user)

    my_projects = Proyecto.objects.filter(artista=artista)
    other_projects = Proyecto.objects.exclude(artista=artista)

    context = {
        'artista': artista,
        'perfil': perfil,
        'my_projects': my_projects,
        'other_projects': other_projects,
    }
    return render(request, 'index.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                perfil = PerfilUsuario.objects.get(user=user)

                # 🔒 Redirigir según el rol
                if perfil.rol == PerfilUsuario.Rol.ADMIN:
                    return redirect('auditoria_view')
                else:
                    return redirect('index_view')
            else:
                messages.error(request, "Cuenta desactivada.")
        else:
            messages.error(request, "Credenciales incorrectas.")
    return render(request, 'login.html')


@login_required(login_url='login_view')
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login_view')


@login_required(login_url='login_view')
def listar_view(request):
    usuario = request.user
    perfil = PerfilUsuario.objects.get(user=usuario)
    artista, _ = Artista.objects.get_or_create(nombre=usuario.username)

    my_projects = Proyecto.objects.filter(artista=artista)
    other_projects = Proyecto.objects.exclude(artista=artista)

    titulo = request.GET.get('titulo', '')
    artista_nombre = request.GET.get('artista', '')
    descripcion = request.GET.get('descripcion', '')
    tipo = request.GET.get('tipo', 'todos')

    proyectos = Proyecto.objects.all()

    if titulo:
        proyectos = proyectos.filter(titulo__icontains=titulo)
    if artista_nombre:
        proyectos = proyectos.filter(artista__nombre__icontains=artista_nombre)
    if descripcion:
        proyectos = proyectos.filter(descripcion__icontains=descripcion)

    if tipo == 'propios':
        proyectos = proyectos.filter(artista=artista)
    elif tipo == 'otros':
        proyectos = proyectos.exclude(artista=artista)

    context = {
        'my_projects': my_projects,
        'other_projects': other_projects,
        'proyectos': proyectos,
        'perfil': perfil,
    }
    return render(request, 'listar.html', context)


@login_required(login_url='login_view')
def crear_proyecto(request):
    perfil = PerfilUsuario.objects.get(user=request.user)

    if perfil.rol not in [PerfilUsuario.Rol.ARTISTA, PerfilUsuario.Rol.ADMIN]:
        messages.error(request, 'Solo los artistas o administradores pueden crear proyectos.')
        return redirect('listar')

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')

        if not titulo:
            messages.error(request, 'El título es obligatorio.')
            return redirect('listar')

        nombre = request.user.username
        artista, _ = Artista.objects.get_or_create(nombre=nombre)

        proyecto = Proyecto.objects.create(
            artista=artista,
            titulo=titulo,
            descripcion=descripcion or '',
            imagen=imagen
        )

        Historial.objects.create(
            usuario=request.user,
            accion='Creó un proyecto',
            tabla_afectada='Proyecto',
            registro_afectado_id=proyecto.id
        )

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
    Historial.objects.create(
        usuario=request.user,
        accion='Eliminó un proyecto',
        tabla_afectada='Proyecto',
        registro_afectado_id=proyecto_id
    )

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

        Historial.objects.create(
            usuario=request.user,
            accion='Editó un proyecto',
            tabla_afectada='Proyecto',
            registro_afectado_id=proyecto.id
        )

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
        colaboracion, created = Colaboracion.objects.get_or_create(proyecto=proyecto, artista=artista_obj)

        if created:
            Historial.objects.create(
                usuario=request.user,
                accion='Agregó colaborador',
                tabla_afectada='Colaboracion',
                registro_afectado_id=colaboracion.id
            )
            messages.success(request, f'Artista {nombre_artista} agregado como colaborador.')
        else:
            messages.info(request, f'El artista {nombre_artista} ya está como colaborador.')

    return redirect('listar')


@login_required(login_url='login_view')
def auditoria_view(request):
    perfil = PerfilUsuario.objects.get(user=request.user)

    if perfil.rol != PerfilUsuario.Rol.ADMIN:
        messages.error(request, 'No tienes permiso para acceder al panel de administración.')
        return redirect('index_view')

    historial = Historial.objects.select_related('usuario').order_by('-fecha_hora')
    context = {'historial': historial, 'perfil': perfil}
    return render(request, 'admin.html', context)
