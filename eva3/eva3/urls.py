
from django.contrib import admin
from django.urls import path
from gestor_artistico import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('listar/', views.listar_view, name='listar'),
    path('agregar/', views.agregar_view, name='agregar'),
    path('panel/', views.admin_view, name='admin_view'),
]
