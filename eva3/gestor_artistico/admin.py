from django.contrib import admin
from gestor_artistico.models import Historial, Artista, Proyecto, Colaboracion, PerfilUsuario, Sugerencia

class ArtistaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    
admin.site.register(Artista, ArtistaAdmin)

class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['titulo']

class ColaboracionAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'artista', 'valor', 'fecha_registro']
    list_filter = ['proyecto', 'artista']
    search_fields = ['proyecto__titulo', 'artista__nombre']

class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol']
    search_fields = ['user__username']
    list_filter = ['rol']

class HistorialAdmin(admin.ModelAdmin):
    list_display = ['fecha_hora', 'usuario', 'accion', 'tabla_afectada', 'registro_afectado_id']
    list_filter = ['accion', 'tabla_afectada', 'fecha_hora']
    search_fields = ['usuario__username', 'accion', 'tabla_afectada']

class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'proyecto', 'colaborador', 'fecha_creacion', 'leida']
    list_filter = ['leida', 'fecha_creacion', 'proyecto']
    search_fields = ['titulo', 'descripcion', 'colaborador__nombre', 'proyecto__titulo']

admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Colaboracion, ColaboracionAdmin)
admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)
admin.site.register(Historial, HistorialAdmin)
admin.site.register(Sugerencia, SugerenciaAdmin)
