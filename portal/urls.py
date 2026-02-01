"""
RUTAS DE API - INFO CAMPUS
Configuración de endpoints para el portal
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MateriaViewSet, 
    InscripcionViewSet, 
    dashboard_tesoreria, 
    metricas_institucionales, # Importada para el Director
    dashboard_profesor,       # Importada para el Profesor
    descargar_estado_cuenta,
    login_view,           
    perfil_usuario        
)

# Configuración del Router para ViewSets
router = DefaultRouter()
router.register(r'materias', MateriaViewSet, basename='materia')
router.register(r'inscripciones', InscripcionViewSet, basename='inscripcion')

urlpatterns = [
    # 1. Autenticación y Perfil
    path('login/', login_view, name='login'),
    path('user/me/', perfil_usuario, name='user-me'),
    
    # 2. Rutas Automáticas (ViewSets)
    path('', include(router.urls)),
    
    # 3. Dashboards de Gestión (Los que "exprimen" el Backend)
    path('finanzas/dashboard/', dashboard_tesoreria, name='dashboard-tesoreria'),
    path('institucional/dashboard/', metricas_institucionales, name='dashboard-institucional'),
    path('profesor/dashboard/', dashboard_profesor, name='dashboard-profesor'),
    
    # 4. Reportes y Documentos Certificados
    path('finanzas/estado-cuenta/', descargar_estado_cuenta, name='descargar-estado-cuenta'),
]