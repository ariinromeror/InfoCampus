import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def otorgar_llaves():
    print("🔑 Asignando llaves maestras a los grupos...")

    # Definimos el diccionario de permisos por grupo
    # 'view' = ver, 'add' = crear, 'change' = editar, 'delete' = borrar
    permisos_por_grupo = {
        'Estudiante': [
            'view_usuario', 'view_carrera', 'view_materia', 
            'view_seccion', 'view_inscripcion', 'view_pago'
        ],
        'Profesor': [
            'view_usuario', 'view_materia', 'view_seccion', 
            'view_inscripcion', 'change_inscripcion' # Para subir notas
        ],
        'Tesorero': [
            'view_usuario', 'view_carrera', 'view_inscripcion', 
            'view_pago', 'add_pago', 'change_pago' # Para cobrar
        ],
        'Director': [
            'view_usuario', 'add_usuario', 'change_usuario',
            'view_carrera', 'add_carrera', 'change_carrera',
            'view_materia', 'add_materia', 'change_materia',
            'view_inscripcion', 'change_inscripcion',
            'view_pago', 'view_periodolectivo'
        ],
        'Coordinador': [
            'view_usuario', 'view_materia', 'add_materia', 
            'change_materia', 'view_seccion', 'add_seccion', 
            'change_seccion', 'view_inscripcion', 'change_inscripcion'
        ]
    }

    for nombre_grupo, codigos in permisos_por_grupo.items():
        grupo = Group.objects.get(name=nombre_grupo)
        print(f"📦 Configurando {nombre_grupo}...")
        
        for cod_permiso in codigos:
            try:
                # El formato de Django es 'accion_modelo'
                accion, modelo = cod_permiso.split('_')
                permiso = Permission.objects.get(codename=cod_permiso)
                grupo.permissions.add(permiso)
            except Permission.DoesNotExist:
                print(f"⚠️  No encontré el permiso: {cod_permiso}")
        
    print("\n✨ ¡Llaves entregadas! Ahora tus grupos ya tienen poder en el Admin.")

if __name__ == '__main__':
    otorgar_llaves()