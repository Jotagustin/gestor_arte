from django.contrib import admin
from django.urls import path
from gestor_artistico import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index_view, name='index_view'),
    path('listar/', views.listar_view, name='listar'),
    path('proyecto/create/', views.crear_proyecto, name='crear_proyecto'),
    path('proyecto/<int:proyecto_id>/delete/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('proyecto/<int:proyecto_id>/editar/', views.editar_proyecto, name='editar_proyecto'),
    path('proyecto/<int:proyecto_id>/add_contributor/', views.agregar_colaborador, name='agregar_colaborador'),
    path('auditoria/', views.auditoria_view, name='auditoria_view'),
    path('admin/crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('diagnostico/', views.diagnostico_sesion, name='diagnostico_sesion'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
