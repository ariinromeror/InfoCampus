from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .models import Usuario, Carrera, Materia, Nota, Asistencia
from .serializers import (
    MateriaDetalleSerializer, 
    NotaSerializer, 
    AsistenciaSerializer
)

# --- SISTEMA DE AUTENTICACIÓN (FASE 1.1 / 2.1) ---

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Punto de entrada principal. Devuelve el perfil completo del usuario
    incluyendo flags de Mora y Beca para el Frontend Camaleón.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        return Response({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'rol': user.rol,
            'en_mora': user.en_mora,
            'es_becado': user.es_becado,
            'porcentaje_beca': user.porcentaje_beca,
            'carrera_nombre': user.carrera.nombre if user.carrera else "General"
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


# --- GESTIÓN ACADÉMICA FILTRADA ---

class MisMateriasViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Muestra materias según el contexto del usuario (Profesor o Estudiante).
    """
    serializer_class = MateriaDetalleSerializer
    permission_classes = [AllowAny] 
    
    def get_queryset(self):
        username = self.request.query_params.get('user')
        if not username:
            return Materia.objects.none()

        user = Usuario.objects.filter(username=username).first()
        if not user:
            return Materia.objects.none()

        # Lógica de Roles:
        if user.rol in ['director', 'coordinador']:
            return Materia.objects.all() # El staff ve todo
        
        if user.rol == 'profesor':
            return Materia.objects.filter(profesor=user)
        
        if user.rol == 'estudiante' and user.carrera:
            return Materia.objects.filter(carrera=user.carrera)
        
        return Materia.objects.none()


# --- CONTROL DE NOTAS Y AUDITORÍA ---

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Punto 2.3: Registramos quién está creando la nota (Auditoría)
        serializer.save(modificado_por=self.request.user if self.request.user.is_authenticated else None)


# --- ASISTENCIA Y QR DINÁMICO ---

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='generar_qr')
    def generar_qr(self, request):
        """
        Punto 2.4: Genera el token que el Frontend convertirá en QR.
        """
        import uuid
        token = f"CAMPUS-{uuid.uuid4().hex[:8].upper()}-2026"
        return Response({
            "token_dinamico": token,
            "expira_en": "60s",
            "status": "active"
        })