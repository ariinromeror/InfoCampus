import os
import django
import csv
import random
from datetime import time

# 1. CONFIGURACIÓN DE ENTORNO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from portal.models import Usuario, Carrera, Materia, CargaAcademica

def asignar_permisos_automatizados():
    print("🛡️  Configurando Seguridad y Permisos RBAC...")
    permisos_roles = {
        'Director': '__all__',
        'Tesorero': ['view_usuario', 'view_cargaacademica', 'add_cargaacademica', 'change_cargaacademica'],
        'Coordinador': ['view_materia', 'add_materia', 'change_materia', 'view_carrera', 'add_carrera', 'change_carrera', 'view_usuario'],
        'Administrativo': ['view_usuario', 'change_usuario', 'view_materia', 'view_cargaacademica'],
        'Profesor': ['view_materia', 'view_usuario', 'view_cargaacademica'],
        'Estudiante': ['view_materia', 'view_cargaacademica']
    }

    for nombre_rol, permisos in permisos_roles.items():
        grupo, _ = Group.objects.get_or_create(name=nombre_rol)
        grupo.permissions.clear()
        if permisos == '__all__':
            todos = Permission.objects.filter(content_type__app_label='portal')
            grupo.permissions.set(todos)
        else:
            for p_code in permisos:
                try:
                    accion, modelo = p_code.split('_')
                    perm = Permission.objects.get(codename=f"{accion}_{modelo}", content_type__app_label='portal')
                    grupo.permissions.add(perm)
                except Exception:
                    continue
        print(f"   ✅ Grupo {nombre_rol}: Configurado.")

def run():
    print("🧹 LIMPIEZA: Reiniciando el instituto para simulación histórica...")
    CargaAcademica.objects.all().delete()
    Materia.objects.all().delete()
    Usuario.objects.exclude(is_superuser=True).delete()
    Carrera.objects.all().delete()
    Group.objects.all().delete()

    # 2. CARGA DE CARRERAS Y MATERIAS (Desde tu CSV)
    print("📚 ACADEMIA: Importando mallas curriculares...")
    try:
        with open('csv_malla.csv', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                carrera_obj, _ = Carrera.objects.get_or_create(
                    nombre=row['carrera'].strip(),
                    defaults={'codigo': row['codigo'].split('-')[0][:4]}
                )
                Materia.objects.create(
                    nombre=row['nombre'].strip(),
                    codigo=row['codigo'].strip(),
                    carrera=carrera_obj,
                    nivel=int(row['semestre'])
                )
    except FileNotFoundError:
        print("❌ ERROR: No se encontró 'csv_malla.csv'.")
        return

    # 3. CARGA DE USUARIOS BASE (Personal del Instituto)
    print("👤 STAFF: Cargando personal administrativo y docente...")
    try:
        with open('csv_usuarios.csv', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                carrera_u = Carrera.objects.filter(nombre=row['carrera'].strip()).first()
                user = Usuario.objects.create_user(
                    username=row['username'].strip(),
                    email=row['email'].strip(),
                    password='password123',
                    rol=row['rol'].strip().lower(),
                    dni=row['dni'].strip(),
                    en_mora=(row['en_mora'].strip() == 'True'),
                    carrera=carrera_u
                )
                grupo_obj, _ = Group.objects.get_or_create(name=row['rol'].strip().capitalize())
                user.groups.add(grupo_obj)
    except FileNotFoundError:
        print("⚠️ AVISO: 'csv_usuarios.csv' no encontrado.")

    # Crear un Profesor Demo para las clases si no hay en el CSV
    profe_demo, _ = Usuario.objects.get_or_create(
        username='profe_asignado',
        defaults={'rol': 'profesor', 'dni': '9999', 'is_staff': True}
    )
    profe_demo.set_password('password123')
    profe_demo.save()

    # 4. GENERACIÓN DE 20 ALUMNOS CON HISTORIA (2025 -> 2026)
    print("🧪 SIMULACIÓN: Generando 20 alumnos con historial académico...")
    carreras = list(Carrera.objects.all())
    grupo_est, _ = Group.objects.get_or_create(name='Estudiante')
    
    for i in range(1, 21):
        carrera_random = random.choice(carreras)
        est = Usuario.objects.create_user(
            username=f"estudiante_{i}",
            email=f"est_{i}@instituto.edu",
            password="password123",
            rol="estudiante",
            dni=f"2025{i:04d}",
            carrera=carrera_random,
            en_mora=random.choice([True, False, False, False])
        )
        est.groups.add(grupo_est)

        # Inscribir en Periodo Pasado (Nivel 1)
        mats_n1 = Materia.objects.filter(carrera=carrera_random, nivel=1)[:5]
        for m in mats_n1:
            CargaAcademica.objects.create(
                estudiante=est,
                profesor=profe_demo,
                materia=m,
                periodo_lectivo="2025-01",
                nota_final=round(random.uniform(5.5, 10.0), 1), # Aprobados
                pagado=True,
                dia=random.choice(['LU', 'MA', 'MI', 'JU', 'VI']),
                hora_inicio=time(8, 0)
            )

        # Inscribir en Periodo Actual (Nivel 2)
        mats_n2 = Materia.objects.filter(carrera=carrera_random, nivel=2)[:5]
        for m in mats_n2:
            CargaAcademica.objects.create(
                estudiante=est,
                profesor=profe_demo,
                materia=m,
                periodo_lectivo="2026-01",
                nota_final=round(random.uniform(0.0, 10.0), 1), # Notas variadas
                pagado=not est.en_mora,
                dia=random.choice(['LU', 'MA', 'MI', 'JU', 'VI']),
                hora_inicio=time(10, 0)
            )

    # 5. SEGURIDAD FINAL
    asignar_permisos_automatizados()

    print("\n" + "="*50)
    print(f"✨ SIMULACIÓN 'INFO-CAMPUS' CARGADA")
    print(f"📊 Total Usuarios: {Usuario.objects.count()}")
    print(f"📊 Total Cargas Académicas: {CargaAcademica.objects.count()}")
    print(f"📅 Periodos: 2025-01 (Historial) y 2026-01 (Actual)")
    print("="*50)

if __name__ == '__main__':
    run()