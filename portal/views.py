from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .models import Usuario, Carrera, Materia, CargaAcademica
from .serializers import UsuarioSerializer, MateriaSerializer, CargaAcademicaSerializer

# --- LOGIN CORREGIDO ---
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        # Verificar que el usuario esté activo
        if not user.is_active:
            return Response({
                'error': 'Usuario inactivo. Contacta a administración.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        token, _ = Token.objects.get_or_create(user=user)
        user_data = UsuarioSerializer(user).data
        
        # ✅ CORRECCIÓN: Devolver 'access' en lugar de 'token'
        return Response({
            'access': token.key,  # Frontend espera 'access'
            'refresh': token.key, # Por compatibilidad (aunque no uses JWT)
            'user': user_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'detail': 'Credenciales inválidas'  # Frontend busca 'detail'
    }, status=status.HTTP_401_UNAUTHORIZED)

# --- VISTA DE PERFIL ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    try:
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- VISTA DE MATERIAS ---
class MateriaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MateriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'estudiante':
            if user.en_mora:
                return Materia.objects.none()
            if not user.carrera:
                return Materia.objects.none()
            return Materia.objects.filter(carrera=user.carrera)
        return Materia.objects.all()

# --- VISTA DE CARGA ACADÉMICA ---
class CargaAcademicaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CargaAcademicaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'estudiante':
            if user.en_mora:
                return CargaAcademica.objects.none()
            return CargaAcademica.objects.filter(estudiante=user)
        if user.rol == 'profesor':
            return CargaAcademica.objects.filter(profesor=user)
        return CargaAcademica.objects.all()