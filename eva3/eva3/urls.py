
from django.contrib import admin
from django.urls import path
from gestor_artistico import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index_view, name='index_view'),
    path('listar/', views.listar_view, name='listar'),
    path('agregar/', views.agregar_view, name='agregar'),
    path('panel/', views.admin_view, name='admin_view'),
    path('proyecto/create/', views.crear_proyecto, name='crear_proyecto'),
    path('proyecto/<int:proyecto_id>/delete/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('proyecto/<int:proyecto_id>/editar/', views.editar_proyecto, name='editar_proyecto'),
    path('proyecto/<int:proyecto_id>/add_contributor/', views.agregar_colaborador, name='agregar_colaborador'),
]
