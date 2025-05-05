"""
Configuración de URLs para el proyecto mytestsite.

Este archivo define las rutas principales del proyecto:
- /admin/: Panel de administración de Django
- /: Redirección al panel de administración
"""

# Importaciones necesarias de Django
from django.contrib import admin  # Para el panel de administración
from django.urls import path, include  # Para definir rutas
from django.views.generic import RedirectView  # Para redirecciones

# Definición de las rutas URL del proyecto
urlpatterns = [
    # Ruta para el panel de administración de Django
    path('admin/', admin.site.urls),
    
    # Redireccionar la página principal al panel de administración
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
]
