# Manual de Instalación y Configuración - Sistema Gestor Artístico

## Requisitos del Sistema

### Software Necesario
- Python 3.11 o superior
- MySQL Server 8.0 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

### Sistema Operativo
- Linux (Ubuntu/Debian recomendado)
- Windows 10/11
- macOS

## Pasos de Instalación

### 1. Preparación del Entorno

#### Crear directorio de trabajo
```bash
mkdir gestor_artistico
cd gestor_artistico
```

#### Crear entorno virtual
```bash
python -m venv env
```

#### Activar entorno virtual

**En Linux/macOS:**
```bash
source env/bin/activate
```

**En Windows:**
```bash
env\Scripts\activate
```

### 2. Instalación de Dependencias

#### Dependencias del Proyecto
El sistema requiere los siguientes paquetes Python:

- **Django 5.2.7** - Framework web principal
- **mysqlclient 2.2.7** - Conector para base de datos MySQL
- **Pillow 12.0.0** - Procesamiento de imágenes
- **asgiref 3.10.0** - Soporte ASGI para Django
- **sqlparse 0.5.3** - Parser SQL para Django

#### Instalación manual de dependencias
```bash
pip install Django==5.2.7
pip install mysqlclient==2.2.7
pip install Pillow==12.0.0
pip install asgiref==3.10.0
pip install sqlparse==0.5.3
```

#### Instalación desde archivo requirements.txt (si está disponible)
```bash
pip install -r requirements.txt
```

### 3. Configuración de Base de Datos MySQL

#### Crear base de datos
```sql
-- Conectarse a MySQL como administrador
mysql -u root -p

-- Crear base de datos
CREATE DATABASE Eva3 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario para Django
CREATE USER 'django_user'@'localhost' IDENTIFIED BY '2405';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON Eva3.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;

-- Salir de MySQL
EXIT;
```

#### Verificar conexión
```bash
mysql -u django_user -p2405 Eva3
```

### 4. Configuración del Proyecto Django

#### Ubicarse en el directorio del proyecto
```bash
cd eva3
```

#### Verificar configuración de base de datos
Editar `eva3/settings.py` si es necesario:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Eva3',
        'USER': 'django_user',
        'PASSWORD': '2405',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

#### Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Creación de Superusuario

#### Crear superusuario para el panel de administración
```bash
python manage.py createsuperuser
```

**Datos sugeridos:**
- Usuario: `admin`
- Email: `admin@localhost.com`
- Contraseña: `admin123` (o la que prefiera)

### 6. Poblado de Datos de Prueba

#### Ejecutar comando de poblado automático
```bash
python manage.py poblar_datos_simple
```

Este comando creará automáticamente:
- 3 usuarios de prueba
- 3 perfiles de usuario
- 3 artistas
- 3 proyectos artísticos
- 3 colaboraciones
- 3 sugerencias
- 3 registros de historial

#### Credenciales de usuarios de prueba
- **admin_prueba** / 123456 (Administrador)
- **miguel_artista** / 123456 (Artista)
- **sofia_creativa** / 123456 (Artista)

### 7. Configuración de Archivos Estáticos

#### Crear directorio para archivos multimedia
```bash
mkdir media
```



### 8. Iniciar el Servidor de Desarrollo

#### Ejecutar servidor Django
```bash
python manage.py runserver
```

#### Acceder a la aplicación
- **Aplicación principal:** http://127.0.0.1:8000/
- **Panel de administración:** http://127.0.0.1:8000/admin/

## Verificación de Instalación

### Pruebas básicas a realizar:

1. **Acceso al sistema:** Ingresar con credenciales de prueba
2. **Panel de administración:** Verificar acceso con superusuario
3. **Creación de proyecto:** Crear un nuevo proyecto artístico
4. **Subida de imágenes:** Probar carga de archivos multimedia
5. **Sistema de colaboraciones:** Agregar colaboradores a proyectos
6. **Sistema de sugerencias:** Enviar y recibir sugerencias

## Solución de Problemas Comunes

### Error de conexión MySQL
```bash
# Verificar que MySQL esté ejecutándose
sudo systemctl status mysql

# Iniciar MySQL si está detenido
sudo systemctl start mysql
```

### Error de permisos en archivos multimedia
```bash
# En Linux, dar permisos al directorio media
chmod 755 media/
```

### Error de dependencias
```bash
# Verificar instalación de dependencias
pip list
pip install --upgrade <paquete>
```


