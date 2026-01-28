from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MateriaViewSet, 
    CargaAcademicaViewSet, 
    perfil_usuario,
    login_view
)

router = DefaultRouter()
router.register(r'materias', MateriaViewSet, basename='materia')
router.register(r'historial', CargaAcademicaViewSet, basename='historial')

urlpatterns = [
    path('login/', login_view, name='login'), 
    path('user/me/', perfil_usuario, name='user-me'),
    path('', include(router.urls)),
]