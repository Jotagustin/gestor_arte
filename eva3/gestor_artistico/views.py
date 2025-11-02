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

    my_projects = Proyecto.objects.filter(artista=artista).prefetch_related('colaboracion_set__artista')
    other_projects = Proyecto.objects.exclude(artista=artista).prefetch_related('colaboracion_set__artista')
    
    # Lista de todos los artistas para el desplegable del modal
    todos_artistas = Artista.objects.all().order_by('nombre')

    context = {
        'artista': artista,
        'perfil': perfil,
        'my_projects': my_projects,
        'other_projects': other_projects,
        'todos_artistas': todos_artistas,
    }
    return render(request, 'index.html', context)


def login_view(request):
    # Si ya está autenticado, redirigir
    if request.user.is_authenticated:
        return redirect('index_view')
        
    if request.method == "POST":
        action = request.POST.get('action', 'login')
        
        if action == 'register':
            # REGISTRO DE NUEVO USUARIO
            return handle_register(request)
        else:
            # LOGIN EXISTENTE
            return handle_login(request)
            
    return render(request, 'login.html')


def handle_register(request):
    """Maneja el registro de nuevos usuarios"""
    username = request.POST.get('username')
    email = request.POST.get('email', '')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    
    # Validaciones
    if not username or not password or not password2:
        messages.error(request, "Complete todos los campos obligatorios.")
        return render(request, 'login.html')
    
    if password != password2:
        messages.error(request, "Las contraseñas no coinciden.")
        return render(request, 'login.html')
    
    if len(password) < 4:
        messages.error(request, "La contraseña debe tener al menos 4 caracteres.")
        return render(request, 'login.html')
    
    try:
        from django.contrib.auth.models import User
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, f"El usuario '{username}' ya existe. Prueba con otro nombre.")
            return render(request, 'login.html')
        
        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        # Crear perfil de artista por defecto
        perfil, created = PerfilUsuario.objects.get_or_create(
            user=user,
            defaults={'rol': PerfilUsuario.Rol.ARTISTA}
        )
        
        # Crear artista asociado
        Artista.objects.get_or_create(nombre=username)
        
        # Registrar en historial
        Historial.objects.create(
            usuario=user,
            accion='Usuario registrado',
            tabla_afectada='User',
            registro_afectado_id=user.id
        )
        
        # Login automático después del registro
        login(request, user)
        request.session.cycle_key()
        
        messages.success(request, f"¡Bienvenido {username}! Tu cuenta de artista ha sido creada exitosamente.")
        return redirect('index_view')
        
    except Exception as e:
        messages.error(request, f"Error al crear la cuenta: {str(e)}")
        return render(request, 'login.html')


def handle_login(request):
    """Maneja el login de usuarios existentes"""
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        messages.error(request, "Por favor, complete todos los campos.")
        return render(request, 'login.html')

    try:
        # Limpiar sesión anterior
        request.session.flush()
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                # Log exitoso, crear nueva sesión
                login(request, user)
                
                # Regenerar session key por seguridad
                request.session.cycle_key()
                
                # Intentar obtener o crear el perfil
                try:
                    perfil = PerfilUsuario.objects.get(user=user)
                except PerfilUsuario.DoesNotExist:
                    # Crear perfil por defecto si no existe
                    perfil = PerfilUsuario.objects.create(
                        user=user,
                        rol=PerfilUsuario.Rol.ARTISTA
                    )
                    messages.info(request, "Se creó automáticamente tu perfil de artista.")

                # Registrar en historial
                Historial.objects.create(
                    usuario=user,
                    accion='Inicio de sesión',
                    tabla_afectada='Usuario',
                    registro_afectado_id=user.id
                )

                # 🔒 Redirigir según el rol
                if perfil.rol == PerfilUsuario.Rol.ADMIN:
                    return redirect('auditoria_view')
                else:
                    return redirect('index_view')
            else:
                messages.error(request, "Cuenta desactivada.")
        else:
            messages.error(request, "Credenciales incorrectas.")
            # Log de intento fallido
            from django.contrib.auth.models import User
            try:
                user_exists = User.objects.filter(username=username).exists()
                if user_exists:
                    messages.error(request, "La contraseña es incorrecta.")
                else:
                    messages.error(request, "El usuario no existe. ¿Quieres crear una cuenta?")
            except:
                pass
                
    except Exception as e:
        messages.error(request, f"Error en el sistema de autenticación. Por favor, contacte al administrador.")
        # Log del error (en producción usarías logging)
        print(f"Error de login: {str(e)}")
        
    return render(request, 'login.html')


@login_required(login_url='login_view')
def logout_view(request):
    username = request.user.username if request.user.is_authenticated else "Usuario"
    logout(request)
    
    # Limpiar sesión completamente
    request.session.flush()
    
    messages.success(request, f"Sesión de {username} cerrada correctamente.")
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

    return redirect('index_view')


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
    
    # Estadísticas adicionales para el admin
    from django.contrib.auth.models import User
    total_usuarios = User.objects.count()
    usuarios_artista = PerfilUsuario.objects.filter(rol=PerfilUsuario.Rol.ARTISTA).count()
    usuarios_admin = PerfilUsuario.objects.filter(rol=PerfilUsuario.Rol.ADMIN).count()
    
    context = {
        'historial': historial, 
        'perfil': perfil,
        'total_usuarios': total_usuarios,
        'usuarios_artista': usuarios_artista,
        'usuarios_admin': usuarios_admin,
    }
    return render(request, 'admin.html', context)


@login_required(login_url='login_view')
def crear_usuario(request):
    """Vista para que los ADMIN puedan crear nuevos usuarios"""
    perfil = PerfilUsuario.objects.get(user=request.user)
    
    if perfil.rol != PerfilUsuario.Rol.ADMIN:
        messages.error(request, 'No tienes permiso para crear usuarios.')
        return redirect('index_view')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email', '')
        rol = request.POST.get('rol')
        
        if not username or not password or not rol:
            messages.error(request, 'Complete todos los campos obligatorios.')
            return render(request, 'crear_usuario.html')
        
        try:

            from django.contrib.auth.models import User
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            PerfilUsuario.objects.create(
                user=user,
                rol=rol
            )

            if rol == PerfilUsuario.Rol.ARTISTA:
                Artista.objects.get_or_create(nombre=username)
            

            Historial.objects.create(
                usuario=request.user,
                accion=f'Creó usuario {username} con rol {rol}',
                tabla_afectada='User',
                registro_afectado_id=user.id
            )
            
            messages.success(request, f'Usuario {username} creado exitosamente con rol {rol}.')
            return redirect('auditoria_view')
            
        except Exception as e:
            messages.error(request, f'Error al crear usuario: {str(e)}')
    
    context = {
        'roles': PerfilUsuario.Rol.choices,
        'perfil': perfil
    }
    return render(request, 'crear_usuario.html', context)


def diagnostico_sesion(request):

    from django.contrib.sessions.models import Session
    from django.contrib.auth.models import User
    from django.utils import timezone
    from django.http import JsonResponse
    
    context = {
        'usuario_actual': str(request.user) if request.user.is_authenticated else 'Anónimo',
        'esta_autenticado': request.user.is_authenticated,
        'sesion_key': request.session.session_key,
        'total_usuarios': User.objects.count(),
        'usuarios_activos': User.objects.filter(is_active=True).count(),
        'total_sesiones': Session.objects.count(),
        'sesiones_expiradas': Session.objects.filter(expire_date__lt=timezone.now()).count(),
        'total_perfiles': PerfilUsuario.objects.count(),
        'usuarios_sin_perfil': User.objects.filter(perfilusuario__isnull=True).count(),
    }
    
    return JsonResponse(context)
