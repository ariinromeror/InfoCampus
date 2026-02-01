"""
VISTAS DE LÓGICA DE NEGOCIO - INFO CAMPUS
Manejo de API, Dashboards por Rol, Permisos y Autenticación
"""

from django.db.models import Sum, F, Q, DecimalField, ExpressionWrapper, Count, Avg
from django.http import FileResponse
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# Importante: Añadimos ValidationError para el bloqueo de seguridad
from rest_framework.exceptions import ValidationError

# Imports Locales
from .models import Usuario, Materia, Inscripcion, Carrera, Seccion
from .serializers import UsuarioSerializer, InscripcionSerializer, MateriaSerializer
from .utils import generar_pdf_estado_cuenta

# ----------------------------------------------------------------
# 1. DASHBOARDS DE GESTIÓN (DIRECTOR, TESORERO, COORDINADOR)
# ----------------------------------------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def metricas_institucionales(request):
    """
    Dashboard para Director y Coordinador.
    Muestra: Total alumnos, alumnos por carrera y materias activas.
    """
    if request.user.rol not in ['director', 'coordinador']:
        return Response({"error": "No autorizado"}, status=403)

    stats = {
        "total_estudiantes": Usuario.objects.filter(rol='estudiante').count(),
        "estudiantes_por_carrera": Carrera.objects.annotate(
            num_alumnos=Count('usuario')
        ).values('nombre', 'num_alumnos'),
        "materias_totales": Materia.objects.count(),
        "promedio_institucional": Inscripcion.objects.aggregate(
            Avg('nota_final')
        )['nota_final__avg'] or 0
    }
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_tesoreria(request):
    """
    Dashboard para el Tesorero.
    Calcula ingresos proyectados vs reales basados en inscripciones y pagos.
    """
    if request.user.rol not in ['director', 'tesorero']:
        return Response({"error": "Acceso denegado"}, status=403)

    # Lógica de cálculo financiero original
    costo_base = ExpressionWrapper(
        F('seccion__materia__creditos') * F('estudiante__carrera__precio_credito'),
        output_field=DecimalField()
    )
    descuento = ExpressionWrapper(
        costo_base * (F('estudiante__porcentaje_beca') / 100.0),
        output_field=DecimalField()
    )
    costo_neto = ExpressionWrapper(
        costo_base - descuento,
        output_field=DecimalField()
    )

    metricas = Inscripcion.objects.annotate(
        monto_a_pagar=costo_neto
    ).aggregate(
        total_proyectado=Sum('monto_a_pagar'),
        total_recaudado=Sum('monto_a_pagar', filter=Q(pago__isnull=False))
    )

    total_p = metricas['total_proyectado'] or 0
    total_r = metricas['total_recaudado'] or 0

    return Response({
        "ingreso_proyectado": f"${total_p:,.2f}",
        "ingreso_real": f"${total_r:,.2f}",
        "tasa_cobranza": f"{(total_r/total_p*100) if total_p > 0 else 0:.1f}%",
        "listado_cobranza": Usuario.objects.filter(rol='estudiante').values(
            'username', 'en_mora', 'deuda_total'
        )
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_profesor(request):
    """
    Dashboard para el Profesor.
    Lista sus secciones actuales y estadísticas de sus alumnos.
    """
    if request.user.rol != 'profesor':
        return Response({"error": "Acceso restringido a profesores"}, status=403)

    secciones_queryset = Seccion.objects.filter(
        profesor=request.user
    ).select_related('materia', 'periodo')

    total_alumnos = Inscripcion.objects.filter(
        seccion__in=secciones_queryset
    ).count()

    promedio_grupal = Inscripcion.objects.filter(
        seccion__in=secciones_queryset
    ).aggregate(Avg('nota_final'))['nota_final__avg'] or 0

    return Response({
        "stats": {
            "secciones_activas": secciones_queryset.count(),
            "total_alumnos": total_alumnos,
            "rendimiento_promedio": round(float(promedio_grupal), 2)
        },
        "mis_clases": [
            {
                "id": s.id,
                "materia": s.materia.nombre,
                "codigo": s.codigo_seccion,
                "aula": s.aula,
                "alumnos_inscritos": s.inscripciones.count(),
                "horario": s.horario_str
            } for s in secciones_queryset
        ]
    })


# ----------------------------------------------------------------
# 2. VIEWSETS (GESTIÓN ACADÉMICA Y SEGURIDAD)
# ----------------------------------------------------------------

class InscripcionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar Inscripciones con seguridad por rol.
    """
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Inscripcion.objects.select_related('seccion', 'seccion__materia', 'estudiante')

        if user.rol == 'estudiante':
            return qs.filter(estudiante=user)
        if user.rol == 'profesor':
            return qs.filter(seccion__profesor=user)
        return qs

    
    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user
       
        nueva_nota = self.request.data.get('nota_final')

        
        if user.rol == 'profesor' and instance.nota_final is not None:
            
            raise ValidationError({
                "error": "El sticker ya está pegado. No puedes cambiar la nota, contacta a tu Coordinador."
            })

        
        if instance.nota_final is None and nueva_nota is not None:
            serializer.save(
                nota_puesta_por=user,
                fecha_nota_puesta=timezone.now()
            )
        
        elif user.rol in ['coordinador', 'director']:
            serializer.save(nota_modificada_por=user)
        else:
            
            serializer.save()

    @action(detail=False, methods=['get'])
    def mi_historial(self, request):
        """ Endpoint extra para ver notas históricas del alumno. """
        inscripciones = self.get_queryset().filter(estado='finalizada')
        serializer = self.get_serializer(inscripciones, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def resumen_academico(self, request):
        """
        Motor de datos centralizado (Fase 1.2).
        Calcula promedios y estados directamente en el servidor.
        """
        user = request.user
        inscripciones = self.get_queryset()
        
        notas = [i.nota_final for i in inscripciones if i.nota_final and i.nota_final > 0]
        promedio = sum(notas) / len(notas) if notas else 0
        
        return Response({
            "promedio_general": round(float(promedio), 2),
            "materias_inscritas": inscripciones.count(),
            "estado_financiero": "MORA" if user.en_mora else "SOLVENTE",
            "deuda_total": float(user.deuda_total)
        })


class MateriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet simple para listar materias disponibles.
    """
    serializer_class = MateriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'estudiante':
            return Materia.objects.filter(carrera=user.carrera)
        return Materia.objects.all()

# ----------------------------------------------------------------
# 3. AUTENTICACIÓN Y PERFIL
# ----------------------------------------------------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """ Login robusto que entrega token y datos de rol. """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'access': token.key,
            'user': UsuarioSerializer(user).data
        }, status=200)
    return Response({'detail': 'Credenciales inválidas'}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    return Response(UsuarioSerializer(request.user).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def descargar_estado_cuenta(request):
    """
    Genera y sirve el PDF del estado de cuenta solo si el usuario no está en mora.
    """
    try:
        if request.user.en_mora:
            return Response(
                {"error": "No puede descargar el reporte teniendo saldos pendientes."}, 
                status=403
            )
        
        pdf = generar_pdf_estado_cuenta(request.user)
        response = FileResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="estado_cuenta.pdf"'
        return response
    except Exception as e:
        return Response({"error": str(e)}, status=500)