from rest_framework import serializers
from .models import Usuario, Carrera, Materia, CargaAcademica

# 1. Serializer de Usuario (Perfil y Login)
class UsuarioSerializer(serializers.ModelSerializer):
    # SerializerMethodField evita que el API explote si el usuario no tiene carrera
    nombre_carrera = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            'id', 
            'username', 
            'first_name', 
            'last_name', 
            'rol', 
            'dni', 
            'en_mora', 
            'es_becado', 
            'nombre_carrera'
        ]

    def get_nombre_carrera(self, obj):
        return obj.carrera.nombre if obj.carrera else "Sin carrera asignada"


# 2. Serializer de Materia (Malla Curricular)
class MateriaSerializer(serializers.ModelSerializer):
    nombre_carrera = serializers.CharField(source='carrera.nombre', read_only=True)
    nombre_prerrequisito = serializers.CharField(source='prerrequisito.nombre', read_only=True, default="Ninguno")

    class Meta:
        model = Materia
        # CORRECCIÓN: 'nivel' existe en tu modelo, 'creditos' NO existe.
        fields = ['id', 'nombre', 'codigo', 'nivel', 'nombre_carrera', 'nombre_prerrequisito']


# 3. Serializer de Carga Académica (Dashboard)
class CargaAcademicaSerializer(serializers.ModelSerializer):
    materia_nombre = serializers.ReadOnlyField(source='materia.nombre')
    materia_codigo = serializers.ReadOnlyField(source='materia.codigo')
    profesor_nombre = serializers.SerializerMethodField()

    class Meta:
        model = CargaAcademica
        fields = [
            'id', 
            'materia_nombre', 
            'materia_codigo', 
            'profesor_nombre',
            'periodo_lectivo', 
            'nota_final', 
            'pagado', 
            'dia', 
            'hora_inicio',
            'seccion',
            'aula'
        ]

    def get_profesor_nombre(self, obj):
        if obj.profesor:
            return f"{obj.profesor.first_name} {obj.profesor.last_name}".strip() or obj.profesor.username
        return "Por asignar"