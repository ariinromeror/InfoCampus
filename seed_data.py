import os
import django

# 1. CONFIGURACIÓN DEL ENTORNO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group
from portal.models import Usuario, Carrera, Materia, Nota

def seed_db():
    print("--- Iniciando Carga del Golden Dataset (Visión 2036) ---")

    # 1. LIMPIEZA DE DATOS (Para evitar duplicados en pruebas)
    print("Limpiando base de datos...")
    Materia.objects.all().delete()
    Carrera.objects.all().delete()
    Usuario.objects.filter(is_superuser=False).delete()
    Group.objects.all().delete()

    # 2. CREACIÓN DE ROLES (RBAC - Fase 1.3)
    print("Configurando Roles (Grupos)...")
    roles = ['Director', 'Coordinador', 'Tesorero', 'Administrativo', 'Profesor', 'Estudiante']
    for rol in roles:
        Group.objects.get_or_create(name=rol)

    # 3. CREACIÓN DE INFRAESTRUCTURA ACADÉMICA
    print("Creando Carreras y Materias...")
    ing_soft = Carrera.objects.create(
        nombre="Ingeniería de Software", 
        codigo="ING-SOFT", 
        descripcion="Carrera base para pruebas SaaS"
    )

    # 4. CREACIÓN DE USUARIOS MAESTROS
    print("Poblando usuarios maestros...")
    
    # El Tesorero (Para Fase 4)
    tesorero = Usuario.objects.create_user(
        username='tesorero_master',
        email='tesoreria@infocampus.edu',
        password='Password123!',
        first_name='Admin',
        last_name='Financiero',
        rol='tesorero'
    )

    # El Profesor
    profe = Usuario.objects.create_user(
        username='profe_suarez',
        email='suarez@infocampus.edu',
        password='Password123!',
        first_name='Carlos',
        last_name='Suárez',
        rol='profesor'
    )

    # Materia vinculada
    prog_1 = Materia.objects.create(
        nombre="Programación I",
        codigo="PROG1",
        carrera=ing_soft,
        profesor=profe,
        metodo_asistencia_default='qr_dinamico'
    )

    # 5. ESTUDIANTES (Casos de Prueba Fase 1.5)
    
    # Estudiante Regular
    Usuario.objects.create_user(
        username='est_regular',
        email='regular@correo.com',
        password='Password123!',
        first_name='Juan',
        last_name='Pérez',
        rol='estudiante',
        carrera=ing_soft,
        en_mora=False
    )

    # Estudiante en Mora (EL CASO CRÍTICO)
    Usuario.objects.create_user(
        username='est_mora',
        email='deudor@correo.com',
        password='Password123!',
        first_name='Pedro',
        last_name='Deudor',
        rol='estudiante',
        carrera=ing_soft,
        en_mora=True  # Flag activo para probar bloqueos
    )

    # Estudiante Becado
    Usuario.objects.create_user(
        username='est_becado',
        email='beca@correo.com',
        password='Password123!',
        first_name='Maria',
        last_name='Excelencia',
        rol='estudiante',
        carrera=ing_soft,
        es_becado=True,
        porcentaje_beca=100
    )

    print("\n--- ¡ÉXITO! ---")
    print(f"Carreras creadas: {Carrera.objects.count()}")
    print(f"Usuarios creados: {Usuario.objects.count()}")
    print(f"Materias creadas: {Materia.objects.count()}")
    print("-------------------------------------------------")
    print("TIP: Usa 'password123!' para todos los usuarios de prueba.")

if __name__ == '__main__':
    seed_db()