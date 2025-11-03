from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import PerfilUsuario


def ensure_user_profile(view_func):
    """
    Decorador que asegura que el usuario autenticado tenga un perfil válido.
    Crea automáticamente un perfil de ARTISTA si no existe.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                # Intentar obtener el perfil
                perfil = request.user.perfilusuario
                # Hacer el perfil disponible en la vista
                request.user_profile = perfil
            except PerfilUsuario.DoesNotExist:
                # Crear perfil automáticamente
                perfil = PerfilUsuario.objects.create(
                    user=request.user,
                    rol=PerfilUsuario.Rol.ARTISTA
                )
                request.user_profile = perfil
                messages.info(request, "Se creó automáticamente tu perfil de artista.")
            except Exception as e:
                # En caso de error grave, redirigir a login
                messages.error(request, "Error con tu perfil de usuario. Por favor, inicia sesión nuevamente.")
                return redirect('login_view')
        
        return view_func(request, *args, **kwargs)
    return wrapper