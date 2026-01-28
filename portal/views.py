from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .models import Usuario, Carrera, Materia, CargaAcademica
from .serializers import UsuarioSerializer, MateriaSerializer, CargaAcademicaSerializer

# --- LOGIN OPTIMIZADO ---
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        # USAMOS EL SERIALIZER AQUÍ PARA MANDAR TODOS LOS DATOS (CARRERA, ROL, ETC)
        user_data = UsuarioSerializer(user).data
        
        return Response({
            'token': token.key,
            'user': user_data
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

# --- VISTA DE PERFIL ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    try:
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)
    except Exception as e:
        # Esto nos ayudará a ver errores en consola si ocurren
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- VISTA DE MATERIAS ---
class MateriaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MateriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'estudiante':
            if user.en_mora:
                return Materia.objects.none()
            # Si el usuario no tiene carrera, no devolvemos nada para evitar error
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