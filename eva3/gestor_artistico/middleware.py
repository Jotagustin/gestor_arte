from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages


class SessionSecurityMiddleware(MiddlewareMixin):

    def process_request(self, request):

        if request.user.is_authenticated:
            try:
 
                if hasattr(request.user, 'perfilusuario'):
                    perfil = request.user.perfilusuario

                    if not perfil:
                        logout(request)
                        messages.error(request, "Sesión invalidada por problemas de perfil.")
                        return redirect('login_view')
                else:
 
                    from .models import PerfilUsuario
                    PerfilUsuario.objects.get_or_create(
                        user=request.user,
                        defaults={'rol': PerfilUsuario.Rol.ARTISTA}
                    )
                    
            except Exception as e:
                logout(request)
                messages.error(request, "Sesión invalidada por problemas técnicos.")
                return redirect('login_view')
                
        return None
        
    def process_response(self, request, response):

        if hasattr(request, 'session') and request.session.modified:
            request.session.save()
        return response