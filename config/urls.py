from django.contrib import admin
from django.urls import path
from portal import views

urlpatterns = [
    # 1. Panel de Administración
    path('admin/', admin.site.urls),

    # 2. Dashboard Principal
    path('', views.dashboard, name='dashboard'),

    # 3. Gestión de Materias
    path('gestion/', views.gestion_materias, name='gestion_materias'),
    path('eliminar-materia/<int:materia_id>/', views.eliminar_materia, name='eliminar_materia'),
    path('editar-materia/<int:materia_id>/', views.editar_materia, name='editar_materia'),

    # 4. Gestión de Estudiantes
    path('estudiantes/', views.gestion_estudiantes, name='gestion_estudiantes'),
    path('eliminar-estudiante/<int:estudiante_id>/', views.eliminar_estudiante, name='eliminar_estudiante'),
    
    # 5. Registro de Notas/Asistencia
    path('registrar-actividad/<int:materia_id>/', views.registrar_actividad, name='registrar_actividad'),

    # 6. Generación de Reporte PDF
    path('descargar-reporte/', views.generar_reporte_pdf, name='generar_reporte_pdf'),

    # 7. Inscribir Estudiante
    path('inscribir-estudiante/', views.inscribir_estudiante, name='inscribir_estudiante'),

]