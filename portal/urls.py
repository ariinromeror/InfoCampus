from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login_view, MisMateriasViewSet, NotaViewSet, AsistenciaViewSet

router = DefaultRouter()
router.register(r'mis-materias', MisMateriasViewSet, basename='mis-materias')
router.register(r'notas', NotaViewSet, basename='notas')
router.register(r'asistencia', AsistenciaViewSet, basename='asistencia')

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', include(router.urls)),
]