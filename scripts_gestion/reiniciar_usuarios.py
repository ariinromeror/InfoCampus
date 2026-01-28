import os
import sys
import django
import random

# 1. Configurar el entorno de Django para que este script pueda "hablar" con la base de datos
# Nos aseguramos de buscar la carpeta 'config' correctamente subiendo un nivel
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group
from portal.models import Usuario, Carrera

def reiniciar_todo():
    print("🚀 INICIANDO PROTOCOLO DE REINICIO DE USUARIOS...")
    
    # --- 1. LIMPIEZA (Borrar usuarios viejos) ---
    # OJO: No borramos a los superusuarios (admin) para que no pierdas acceso total
    count = Usuario.objects.filter(is_superuser=False).delete()
    print(f"🗑️  Se han eliminado {count[0]} usuarios antiguos (limpieza completada).")

    # --- 2. PREPARACIÓN (Asegurar que existan Carreras y Grupos) ---
    carreras = list(Carrera.objects.all())
    if not carreras:
        print("⚠️ ERROR CRÍTICO: No hay carreras en la base de datos.")
        print("   Por favor, entra al Admin y crea al menos una carrera (Ingeniería, Derecho, etc).")
        return

    # Definimos los roles exactos que tienes en tu Django Admin
    nombres_grupos = ['Administrativo', 'Coordinador', 'Director', 'Estudiante', 'Profesor', 'Tesorero']
    grupos_db = {}
    
    for nombre in nombres_grupos:
        grp, created = Group.objects.get_or_create(name=nombre)
        grupos_db[nombre] = grp

    # --- 3. FABRICACIÓN DE USUARIOS ---
    usuarios_nuevos = []
    contrasena_comun = "Campus2026*" # Una clave segura para todos

    def crear_humano(username, nombre, apellido, nombre_rol, es_staff=False, carrera_obj=None, mora=False):
        # Crear el usuario en la base de datos
        nuevo_usuario = Usuario.objects.create_user(
            username=username,
            password=contrasena_comun,
            first_name=nombre,
            last_name=apellido,
            rol=nombre_rol.lower(), # Guardamos 'estudiante' en minúscula en el campo rol
            dni=f"{random.randint(10000000, 99999999)}",
            is_staff=es_staff,
            carrera=carrera_obj, # Solo estudiantes y coordinadores suelen tener carrera
            en_mora=mora
        )
        # Asignar al Grupo de Django (Para permisos)
        nuevo_usuario.groups.add(grupos_db[nombre_rol])
        
        # Guardar en la lista para el reporte
        usuarios_nuevos.append({
            "usuario": username,
            "clave": contrasena_comun,
            "rol": nombre_rol,
            "nombre": f"{nombre} {apellido}"
        })
        print(f"✅ Creado: {username} ({nombre_rol})")

    # A) CREAR DIRECTORES
    crear_humano("director_general", "Roberto", "Director", "Director", es_staff=True)

    # B) CREAR ADMINISTRATIVOS
    crear_humano("admin_sede", "Laura", "Admin", "Administrativo", es_staff=True)

    # C) CREAR TESOREROS
    crear_humano("tesorero_jefe", "Pedro", "Plata", "Tesorero", es_staff=True)

    # D) CREAR COORDINADORES (Uno por carrera disponible, max 3)
    for i, carrera in enumerate(carreras[:3]):
        crear_humano(f"coord_{carrera.codigo.lower()}", "Coord", carrera.nombre, "Coordinador", es_staff=True, carrera_obj=carrera)

    # E) CREAR PROFESORES (5 Profesores)
    for i in range(1, 6):
        crear_humano(f"profe_{i}", "Profesor", f"Num_{i}", "Profesor", es_staff=True)

    # F) CREAR ESTUDIANTES (10 Estudiantes)
    for i in range(1, 11):
        carrera_random = random.choice(carreras)
        # El estudiante 3 y 8 estarán en mora para probar las alertas
        tiene_mora = True if i in [3, 8] else False 
        crear_humano(f"estudiante_{i}", "Alumno", f"Apellido_{i}", "Estudiante", es_staff=False, carrera_obj=carrera_random, mora=tiene_mora)

    # --- 4. GENERAR REPORTE .TXT ---
    ruta_archivo = os.path.join(os.path.dirname(__file__), '..', 'lista_usuarios_creados.txt')
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write("==================================================\n")
        f.write("      CREDENCIALES DE ACCESO - INFO CAMPUS        \n")
        f.write("==================================================\n\n")
        for u in usuarios_nuevos:
            f.write(f"Rol:      {u['rol']}\n")
            f.write(f"Usuario:  {u['usuario']}\n")
            f.write(f"Clave:    {u['clave']}\n")
            f.write(f"Nombre:   {u['nombre']}\n")
            f.write("--------------------------------------------------\n")
    
    print(f"\n📄 ¡LISTO! Archivo generado en: {ruta_archivo}")

if __name__ == "__main__":
    reiniciar_todo()