from django.contrib import admin
from django.urls import path
from portal import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ==========================================================
    # 1. Administración de Django y Autenticación
    # ==========================================================
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # ==========================================================
    # 2. Dashboard Principal
    # ==========================================================
    path('', views.dashboard, name='dashboard'),

    # ==========================================================
    # 3. Gestión de Materias (CRUD)
    # ==========================================================
    path('materias/', views.gestion_materias, name='gestion_materias'),
    # Nota: Si agregaste la vista editar_materia que mencionaste antes, se mantiene así:
    path('editar-materia/<int:materia_id>/', views.editar_materia, name='editar_materia'), 
    path('eliminar-materia/<int:materia_id>/', views.eliminar_materia, name='eliminar_materia'),

    # ==========================================================
    # 4. Gestión de Estudiantes
    # ==========================================================
    path('estudiantes/', views.gestion_estudiantes, name='gestion_estudiantes'),
    path('eliminar-estudiante/<int:estudiante_id>/', views.eliminar_estudiante, name='eliminar_estudiante'),
    
    # ==========================================================
    # 5. Procesos Académicos (Inscripción y Notas)
    # ==========================================================
    path('inscribir-estudiante/', views.inscribir_estudiante, name='inscribir_estudiante'),
    path('registrar-nota/', views.registrar_nota, name='registrar_nota'),

    # ==========================================================
    # 6. Reportes y Exportación
    # ==========================================================
    path('descargar-reporte/', views.generar_reporte_pdf, name='generar_reporte_pdf'),
]