"""
Configuración principal del proyecto mytestsite.

Este archivo contiene la configuración básica de Django incluyendo:
- Configuración de la base de datos
- Configuración de idioma y zona horaria
- Configuración de aplicaciones instaladas
- Configuración de seguridad
"""

from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

#####################################
# CONFIGURACIÓN DE SEGURIDAD
#####################################

# ADVERTENCIA: Mantener la clave secreta en producción
SECRET_KEY = 'django-insecure-^%7_1c3kd$^#q=gep8iex_fsjpfw@6wdq!29n$8$hwn95)x(o@'

# ADVERTENCIA: No ejecutar con debug activado en producción
DEBUG = True

# Hosts permitidos (vacío permite localhost)
ALLOWED_HOSTS = []

#####################################
# APLICACIONES INSTALADAS
#####################################

INSTALLED_APPS = [
    # Aplicaciones del núcleo de Django
    'django.contrib.admin',  # Panel de administración
    'django.contrib.auth',   # Sistema de autenticación
    'django.contrib.contenttypes',  # Framework de tipos de contenido
    'django.contrib.sessions',  # Framework de sesiones
    'django.contrib.messages',  # Framework de mensajes
    'django.contrib.staticfiles',  # Manejo de archivos estáticos
    
    # Nuestras aplicaciones
    'agro_management.apps.AgroManagementConfig',  # Sistema de gestión agrícola
]

#####################################
# MIDDLEWARE
#####################################

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Seguridad
    'django.contrib.sessions.middleware.SessionMiddleware',  # Sesiones
    'django.middleware.common.CommonMiddleware',  # Funcionalidad común
    'django.middleware.csrf.CsrfViewMiddleware',  # Protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autenticación
    'django.contrib.messages.middleware.MessageMiddleware',  # Mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protección clickjacking
]

# Configuración de URLs raíz
ROOT_URLCONF = 'mytestsite.urls'

#####################################
# PLANTILLAS
#####################################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración WSGI
WSGI_APPLICATION = 'mytestsite.wsgi.application'

#####################################
# BASE DE DATOS
#####################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Motor de base de datos
        'NAME': BASE_DIR / 'db.sqlite3',  # Archivo de la base de datos
    }
}

#####################################
# VALIDACIÓN DE CONTRASEÑAS
#####################################

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#####################################
# INTERNACIONALIZACIÓN
#####################################

# Idioma del sistema
LANGUAGE_CODE = 'es'

# Zona horaria
TIME_ZONE = 'America/Bogota'

# Activar internacionalización
USE_I18N = True

# Usar zona horaria
USE_TZ = True

#####################################
# ARCHIVOS ESTÁTICOS
#####################################

# URL para archivos estáticos
STATIC_URL = 'static/'

# Tipo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
