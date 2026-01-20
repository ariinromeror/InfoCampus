from django.contrib import admin
from django.urls import path
from portal import views  # Importación limpia para evitar errores

urlpatterns = [
    # 1. Panel de Administración
    path('admin/', admin.site.urls),

    # 2. Dashboard Principal
    path('', views.dashboard, name='dashboard'),

    # 3. Gestión de Materias (Listar y Crear)
    path('gestion/', views.gestion_materias, name='gestion_materias'),

    # 4. Acción de Eliminar (Ruta Dinámica)
    # El <int:materia_id> permite pasar el ID de la materia directamente a la función
    path('eliminar-materia/<int:materia_id>/', views.eliminar_materia, name='eliminar_materia'),
]