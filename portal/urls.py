from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login_view, MateriaViewSet

router = DefaultRouter()
router.register(r'academico', MateriaViewSet, basename='academico')

urlpatterns = [
    path('auth/login/', login_view, name='login'),
    path('', include(router.urls)),
]