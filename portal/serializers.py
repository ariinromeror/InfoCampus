from rest_framework import serializers
from .models import Usuario, Carrera, Materia, CargaAcademica

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'rol', 'dni', 'en_mora', 'es_becado', 'carrera']

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = '__all__'

class CargaAcademicaSerializer(serializers.ModelSerializer):
    materia_nombre = serializers.ReadOnlyField(source='materia.nombre')
    materia_codigo = serializers.ReadOnlyField(source='materia.codigo')

    class Meta:
        model = CargaAcademica
        fields = [
            'id', 'materia_nombre', 'materia_codigo', 'periodo_lectivo', 
            'nota_final', 'pagado', 'dia', 'hora_inicio'
        ]