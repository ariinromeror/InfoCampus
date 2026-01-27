from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Usuario, Carrera, Materia, CargaAcademica
from rest_framework.permissions import IsAuthenticated

# --- MIXIN DE SEGURIDAD (RBAC) ---
class RoleRequiredMixin:
    """Permite filtrar el acceso por el campo 'rol' del usuario"""
    def check_role(self, user, allowed_roles):
        return user.is_authenticated and user.rol in allowed_roles

# --- VISTAS DE LÓGICA DE NEGOCIO ---

class MateriaViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # 1. Lógica Estudiante: Filtra por su carrera y bloquea si está en mora
        if user.rol == 'estudiante':
            if user.en_mora:
                return Materia.objects.none() # No ve nada si debe dinero
            return Materia.objects.filter(carrera=user.carrera)
        
        # 2. Lógica Profesor: Solo ve materias que tiene asignadas en CargaAcademica
        if user.rol == 'profesor':
            materias_ids = CargaAcademica.objects.filter(profesor=user).values_list('materia_id', flat=True)
            return Materia.objects.filter(id__in=materias_ids)
            
        # 3. Staff: Ve todo
        return Materia.objects.all()

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    # Aquí irá la integración con JWT después, pero el endpoint ya es fijo
    return Response({"status": "ready", "roles_disponibles": ["estudiante", "profesor", "tesorero", "director"]})