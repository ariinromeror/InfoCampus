"""
SCRIPT 3: Crear Usuarios Organizados por Rol
Genera usuarios con roles y guarda credenciales en usuarios_credenciales.txt
"""

import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portal.models import Usuario, Carrera
from django.contrib.auth.models import Group

def crear_usuarios():
    print("\n" + "=" * 80)
    print("SCRIPT 3: CREANDO USUARIOS POR ROL")
    print("=" * 80 + "\n")
    
    PASSWORD = "campus2026"  # Contraseña para TODOS
    
    carreras = list(Carrera.objects.all())
    
    if not carreras:
        print("❌ ERROR: No hay carreras. Ejecuta primero el script 1 y 2.")
        return
    
    carreras_dict = {c.codigo: c for c in carreras}
    grupos = {
        'Director': Group.objects.get(name='Director'),
        'Coordinador': Group.objects.get(name='Coordinador'),
        'Tesorero': Group.objects.get(name='Tesorero'),
        'Administrativo': Group.objects.get(name='Administrativo'),
        'Profesor': Group.objects.get(name='Profesor'),
        'Estudiante': Group.objects.get(name='Estudiante'),
    }
    
    usuarios_creados = []
    
    # ==================== DIRECTORES (2) ====================
    print("👑 CREANDO DIRECTORES...")
    directores = [
        {"username": "director_01", "nombre": "Carlos", "apellido": "Mendoza", "dni": "11111111"},
        {"username": "director_02", "nombre": "Ana", "apellido": "Torres", "dni": "11111112"},
    ]
    
    for data in directores:
        usuario = Usuario.objects.create_user(
            username=data["username"],
            password=PASSWORD,
            first_name=data["nombre"],
            last_name=data["apellido"],
            rol='director',
            dni=data["dni"],
            is_staff=True
        )
        usuario.groups.add(grupos['Director'])
        usuarios_creados.append({
            'username': data["username"],
            'password': PASSWORD,
            'nombre': f"{data['nombre']} {data['apellido']}",
            'rol': 'Director',
            'dni': data['dni']
        })
        print(f"  ✅ {data['username']} - {data['nombre']} {data['apellido']}")
    
    # ==================== COORDINADORES (5 - uno por carrera) ====================
    print("\n📋 CREANDO COORDINADORES...")
    coordinadores = [
        {"username": "coord_01", "nombre": "María", "apellido": "Ramírez", "carrera": "ADM", "dni": "22222221"},
        {"username": "coord_02", "nombre": "Pedro", "apellido": "González", "carrera": "ING", "dni": "22222222"},
        {"username": "coord_03", "nombre": "Laura", "apellido": "Fernández", "carrera": "MED", "dni": "22222223"},
        {"username": "coord_04", "nombre": "Jorge", "apellido": "Vargas", "carrera": "DER", "dni": "22222224"},
        {"username": "coord_05", "nombre": "Sofía", "apellido": "Castro", "carrera": "PSI", "dni": "22222225"}
    ]
    
    for data in coordinadores:
        carrera = carreras_dict.get(data["carrera"], carreras[0])
        usuario = Usuario.objects.create_user(
            username=data["username"],
            password=PASSWORD,
            first_name=data["nombre"],
            last_name=data["apellido"],
            rol='coordinador',
            dni=data["dni"],
            carrera=carrera,
            is_staff=True
        )
        usuario.groups.add(grupos['Coordinador'])
        usuarios_creados.append({
            'username': data["username"],
            'password': PASSWORD,
            'nombre': f"{data['nombre']} {data['apellido']}",
            'rol': 'Coordinador',
            'carrera': carrera.nombre,
            'dni': data['dni']
        })
        print(f"  ✅ {data['username']} - {data['nombre']} {data['apellido']} ({carrera.codigo})")
    
    # ==================== TESOREROS (2) ====================
    print("\n💰 CREANDO TESOREROS...")
    tesoreros = [
        {"username": "tesorero_01", "nombre": "Carmen", "apellido": "Rojas", "dni": "33333331"},
        {"username": "tesorero_02", "nombre": "Luis", "apellido": "Morales", "dni": "33333332"}
    ]
    
    for data in tesoreros:
        usuario = Usuario.objects.create_user(
            username=data["username"],
            password=PASSWORD,
            first_name=data["nombre"],
            last_name=data["apellido"],
            rol='tesorero',
            dni=data["dni"],
            is_staff=True
        )
        usuario.groups.add(grupos['Tesorero'])
        usuarios_creados.append({
            'username': data["username"],
            'password': PASSWORD,
            'nombre': f"{data['nombre']} {data['apellido']}",
            'rol': 'Tesorero',
            'dni': data['dni']
        })
        print(f"  ✅ {data['username']} - {data['nombre']} {data['apellido']}")
    
    # ==================== ADMINISTRATIVOS (2) ====================
    print("\n📄 CREANDO ADMINISTRATIVOS...")
    administrativos = [
        {"username": "admin_01", "nombre": "Isabel", "apellido": "Ortiz", "dni": "44444441"},
        {"username": "admin_02", "nombre": "Diego", "apellido": "Herrera", "dni": "44444442"}
    ]
    
    for data in administrativos:
        usuario = Usuario.objects.create_user(
            username=data["username"],
            password=PASSWORD,
            first_name=data["nombre"],
            last_name=data["apellido"],
            rol='administrativo',
            dni=data["dni"],
            is_staff=True
        )
        usuario.groups.add(grupos['Administrativo'])
        usuarios_creados.append({
            'username': data["username"],
            'password': PASSWORD,
            'nombre': f"{data['nombre']} {data['apellido']}",
            'rol': 'Administrativo',
            'dni': data['dni']
        })
        print(f"  ✅ {data['username']} - {data['nombre']} {data['apellido']}")
    
    # ==================== PROFESORES (10) ====================
    print("\n👨‍🏫 CREANDO PROFESORES...")
    nombres_prof = ["Miguel", "Isabel", "Diego", "Carmen", "Luis", 
                    "Valentina", "Roberto", "Daniela", "Fernando", "Gabriela"]
    apellidos_prof = ["Silva", "Romero", "Morales", "Ortiz", "Díaz",
                     "Reyes", "Herrera", "Campos", "Navarro", "Ramos"]
    
    for i in range(10):
        username = f"prof_{i+1:02d}"
        carrera = carreras[i % len(carreras)]  # Distribuir
        
        usuario = Usuario.objects.create_user(
            username=username,
            password=PASSWORD,
            first_name=nombres_prof[i],
            last_name=apellidos_prof[i],
            rol='profesor',
            dni=f"5555{i+1:04d}",
            carrera=carrera,
            is_staff=True
        )
        usuario.groups.add(grupos['Profesor'])
        usuarios_creados.append({
            'username': username,
            'password': PASSWORD,
            'nombre': f"{nombres_prof[i]} {apellidos_prof[i]}",
            'rol': 'Profesor',
            'carrera': carrera.nombre,
            'dni': f"5555{i+1:04d}"
        })
        print(f"  ✅ {username} - {nombres_prof[i]} {apellidos_prof[i]} ({carrera.codigo})")
    
    # ==================== ESTUDIANTES (25) ====================
    print("\n🎓 CREANDO ESTUDIANTES...")
    nombres_est = [
        "Juan", "María", "Carlos", "Ana", "Pedro", "Sofía", "Luis", "Carmen",
        "Diego", "Laura", "Miguel", "Isabel", "Jorge", "Valentina", "Andrés",
        "Daniela", "Roberto", "Gabriela", "Fernando", "Camila", "Ricardo",
        "Patricia", "Javier", "Mónica", "Alejandro"
    ]
    apellidos_est = [
        "González", "Rodríguez", "Pérez", "Fernández", "López", "Martínez",
        "Sánchez", "Ramírez", "Torres", "Flores", "Rivera", "Gómez", "Díaz",
        "Vargas", "Castro", "Rojas", "Morales", "Ortiz", "Silva", "Reyes",
        "Herrera", "Campos", "Navarro", "Ramos", "Gutiérrez"
    ]
    
    for i in range(25):
        username = f"est_{i+1:02d}"
        carrera = carreras[i % len(carreras)]
        es_becado = (i % 4 == 0)  # 25% becados
        porcentaje_beca = random.choice([25, 50, 75]) if es_becado else 0
        
        usuario = Usuario.objects.create_user(
            username=username,
            password=PASSWORD,
            first_name=nombres_est[i],
            last_name=apellidos_est[i],
            rol='estudiante',
            dni=f"6666{i+1:04d}",
            carrera=carrera,
            es_becado=es_becado,
            porcentaje_beca=porcentaje_beca
        )
        usuario.groups.add(grupos['Estudiante'])
        
        estado = f"BECA {porcentaje_beca}%" if es_becado else "Regular"
        
        usuarios_creados.append({
            'username': username,
            'password': PASSWORD,
            'nombre': f"{nombres_est[i]} {apellidos_est[i]}",
            'rol': 'Estudiante',
            'carrera': carrera.nombre,
            'dni': f"6666{i+1:04d}",
            'estado': estado
        })
        print(f"  ✅ {username} - {nombres_est[i]} {apellidos_est[i]} ({carrera.codigo}) {estado}")
    
    # ==================== GUARDAR TXT ====================
    print("\n📄 GENERANDO archivo usuarios_credenciales.txt...")
    
    with open('usuarios_credenciales.txt', 'w', encoding='utf-8') as archivo:
        archivo.write("=" * 100 + "\n")
        archivo.write("INFO CAMPUS - CREDENCIALES DE ACCESO\n")
        archivo.write(f"Contraseña para TODOS: {PASSWORD}\n")
        archivo.write(f"Total: {len(usuarios_creados)} usuarios\n")
        archivo.write("=" * 100 + "\n\n")
        
        roles_orden = ['Director', 'Coordinador', 'Tesorero', 'Administrativo', 'Profesor', 'Estudiante']
        
        for rol in roles_orden:
            usuarios_rol = [u for u in usuarios_creados if u['rol'] == rol]
            
            if not usuarios_rol:
                continue
            
            archivo.write(f"\n{'=' * 100}\n")
            archivo.write(f"{rol.upper()}S ({len(usuarios_rol)})\n")
            archivo.write(f"{'=' * 100}\n\n")
            
            for user in usuarios_rol:
                archivo.write(f"Username:  {user['username']}\n")
                archivo.write(f"Password:  {user['password']}\n")
                archivo.write(f"Nombre:    {user['nombre']}\n")
                archivo.write(f"DNI:       {user['dni']}\n")
                if 'carrera' in user:
                    archivo.write(f"Carrera:   {user['carrera']}\n")
                if 'estado' in user:
                    archivo.write(f"Estado:    {user['estado']}\n")
                archivo.write("-" * 100 + "\n\n")
    
    # RESUMEN
    print("\n" + "=" * 80)
    print("✅ USUARIOS CREADOS")
    print("=" * 80)
    print(f"👑 Directores:      {len([u for u in usuarios_creados if u['rol'] == 'Director'])}")
    print(f"📋 Coordinadores:   {len([u for u in usuarios_creados if u['rol'] == 'Coordinador'])}")
    print(f"💰 Tesoreros:       {len([u for u in usuarios_creados if u['rol'] == 'Tesorero'])}")
    print(f"📄 Administrativos: {len([u for u in usuarios_creados if u['rol'] == 'Administrativo'])}")
    print(f"👨‍🏫 Profesores:      {len([u for u in usuarios_creados if u['rol'] == 'Profesor'])}")
    print(f"🎓 Estudiantes:     {len([u for u in usuarios_creados if u['rol'] == 'Estudiante'])}")
    print(f"\n📊 TOTAL:           {len(usuarios_creados)} usuarios")
    print(f"\n📄 Archivo generado: usuarios_credenciales.txt")
    print(f"🔑 Contraseña para todos: {PASSWORD}")
    print("\n📌 Siguiente paso: Ejecutar script 4 (simular_periodos.py)")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    crear_usuarios()