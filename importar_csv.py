import os
import django
import csv

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portal.models import Usuario, Carrera
from django.contrib.auth.models import Group

def importar():
    with open('usuarios_maestros.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # 1. Asegurar que la carrera existe
            carrera, _ = Carrera.objects.get_or_create(
                nombre=row['carrera'], 
                defaults={'codigo': row['carrera'][:3].upper()}
            )
            
            # 2. Crear el usuario
            user, created = Usuario.objects.get_or_create(
                username=row['username'],
                defaults={
                    'email': row['email'],
                    'dni': row['dni'],
                    'rol': row['rol'],
                    'en_mora': row['en_mora'] == 'True',
                    'es_becado': row['es_becado'] == 'True',
                    'porcentaje_beca': int(row['porcentaje_beca']),
                    'carrera': carrera
                }
            )
            
            if created:
                user.set_password('pass1234')
                user.save()
                print(f"👤 Usuario {user.username} creado.")
            else:
                print(f"🟡 El usuario {user.username} ya existe, actualizando grupo...")

            # 3. Asignar al Grupo (Siempre, para asegurar RBAC)
            nombre_grupo = row['rol'].capitalize()
            grupo, _ = Group.objects.get_or_create(name=nombre_grupo)
            if not user.groups.filter(name=nombre_grupo).exists():
                user.groups.add(grupo)
                print(f"  -> Asignado a grupo {nombre_grupo}")

if __name__ == "__main__":
    importar()