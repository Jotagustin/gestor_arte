from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gestor_artistico.models import Artista, Proyecto, Colaboracion, PerfilUsuario, Historial, Sugerencia


class Command(BaseCommand):
    def handle(self, *args, **options):
        
        lista_usuarios = [
            User(username="admin_prueba", email="admin@test.com", first_name="Admin", last_name="Sistema", is_staff=True),
            User(username="miguel_artista", email="miguel@test.com", first_name="Miguel", last_name="Rodríguez"),
            User(username="sofia_creativa", email="sofia@test.com", first_name="Sofia", last_name="González"),
        ]
        
        for user in lista_usuarios:
            user.set_password('123456')
        
        User.objects.bulk_create(lista_usuarios, ignore_conflicts=True)
        
        usuarios_creados = User.objects.filter(username__in=["admin_prueba", "miguel_artista", "sofia_creativa"])
        lista_perfiles = []
        for user in usuarios_creados:
            if user.username == "admin_prueba": 
                lista_perfiles.append(PerfilUsuario(user=user, rol="Admin"))
            else:
                lista_perfiles.append(PerfilUsuario(user=user, rol="Artista"))
        
        PerfilUsuario.objects.bulk_create(lista_perfiles, ignore_conflicts=True)
        
        lista_artistas = [
            Artista(nombre="admin_prueba"),
            Artista(nombre="miguel_artista"),
            Artista(nombre="sofia_creativa"),
        ]
        Artista.objects.bulk_create(lista_artistas, ignore_conflicts=True)
        
        artistas_creados = Artista.objects.filter(nombre__in=["admin_prueba", "miguel_artista", "sofia_creativa"])
        miguel = artistas_creados.get(nombre="miguel_artista")
        sofia = artistas_creados.get(nombre="sofia_creativa")
        admin = artistas_creados.get(nombre="admin_prueba")
        
        lista_proyectos = [
            Proyecto(titulo="Paisajes Urbanos", descripcion="Serie de pinturas urbanas modernas", artista=miguel),
            Proyecto(titulo="Esculturas Recicladas", descripcion="Arte ecológico con materiales reciclados", artista=sofia),
            Proyecto(titulo="Arte Digital", descripcion="Instalaciones interactivas digitales", artista=admin),
        ]
        Proyecto.objects.bulk_create(lista_proyectos, ignore_conflicts=True)
        
        proyectos_creados = Proyecto.objects.filter(titulo__in=["Paisajes Urbanos", "Esculturas Recicladas", "Arte Digital"])
        paisajes = proyectos_creados.get(titulo="Paisajes Urbanos")
        esculturas = proyectos_creados.get(titulo="Esculturas Recicladas")
        
        lista_colaboraciones = [
            Colaboracion(proyecto=paisajes, artista=sofia),
            Colaboracion(proyecto=esculturas, artista=miguel),
            Colaboracion(proyecto=paisajes, artista=admin),
        ]
        Colaboracion.objects.bulk_create(lista_colaboraciones, ignore_conflicts=True)
        
        lista_sugerencias = [
            Sugerencia(proyecto=paisajes, colaborador=sofia, titulo="Mejorar iluminación", descripcion="Sería bueno agregar más contraste en las sombras"),
            Sugerencia(proyecto=esculturas, colaborador=miguel, titulo="Usar más colores", descripcion="Podrías incorporar elementos de color en las esculturas"),
            Sugerencia(proyecto=paisajes, colaborador=admin, titulo="Ampliar serie", descripcion="Esta serie tiene potencial para expandirse a más ciudades"),
        ]
        Sugerencia.objects.bulk_create(lista_sugerencias, ignore_conflicts=True)
        
        usuarios_para_historial = User.objects.filter(username__in=["admin_prueba", "miguel_artista", "sofia_creativa"])
        admin_user = usuarios_para_historial.get(username="admin_prueba")
        miguel_user = usuarios_para_historial.get(username="miguel_artista")
        sofia_user = usuarios_para_historial.get(username="sofia_creativa")
        
        lista_historial = [
            Historial(usuario=miguel_user, accion="Creó proyecto Paisajes Urbanos", tabla_afectada="Proyecto"),
            Historial(usuario=sofia_user, accion="Creó proyecto Esculturas Recicladas", tabla_afectada="Proyecto"),
            Historial(usuario=admin_user, accion="Agregó colaborador a proyecto", tabla_afectada="Colaboracion"),
        ]
        Historial.objects.bulk_create(lista_historial, ignore_conflicts=True)
        
        self.stdout.write('Datos registrados correctamente!')