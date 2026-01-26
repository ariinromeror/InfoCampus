from rest_framework import serializers
from .models import Usuario, Carrera, Materia, Nota, Asistencia

class MateriaDetalleSerializer(serializers.ModelSerializer):
    profesor_nombre = serializers.ReadOnlyField(source='profesor.get_full_name')
    nota_valor = serializers.SerializerMethodField()
    codigo_carrera = serializers.ReadOnlyField(source='carrera.codigo')

    class Meta:
        model = Materia
        fields = ['id', 'nombre', 'profesor_nombre', 'nota_valor', 'codigo_carrera']

    def get_nota_valor(self, obj):
        # DINÁMICO: Obtenemos el usuario que hace la petición
        request = self.context.get('request')
        user_param = request.query_params.get('user') if request else None
        
        if user_param:
            user = Usuario.objects.filter(username=user_param).first()
            if user:
                nota = Nota.objects.filter(estudiante=user, materia=obj).first()
                return float(nota.valor) if nota else 0.0
        return 0.0

class NotaSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.ReadOnlyField(source='estudiante.get_full_name')
    materia_nombre = serializers.ReadOnlyField(source='materia.nombre')
    
    class Meta:
        model = Nota
        fields = [
            'id', 'estudiante', 'estudiante_nombre', 'materia', 
            'materia_nombre', 'valor', 'fecha_registro', 'fecha_modificacion'
        ]

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'