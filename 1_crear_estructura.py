"""
SCRIPT 1: Crear Estructura Base
Crea carreras y periodos lectivos
"""

import os
import django
from decimal import Decimal
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portal.models import Carrera
from django.contrib.auth.models import Group

def crear_estructura():
    print("\n" + "=" * 80)
    print("SCRIPT 1: CREANDO ESTRUCTURA BASE")
    print("=" * 80 + "\n")
    
    # 1. CREAR CARRERAS
    print("📚 Creando Carreras...")
    
    carreras_config = [
        {
            'nombre': 'Administración de Empresas',
            'codigo': 'ADM',
            'precio_credito': Decimal('45.00')
        },
        {
            'nombre': 'Ingeniería en Sistemas',
            'codigo': 'ING',
            'precio_credito': Decimal('60.00')  # Más cara
        },
        {
            'nombre': 'Medicina',
            'codigo': 'MED',
            'precio_credito': Decimal('75.00')  # La más cara
        },
        {
            'nombre': 'Derecho',
            'codigo': 'DER',
            'precio_credito': Decimal('50.00')
        },
        {
            'nombre': 'Psicología',
            'codigo': 'PSI',
            'precio_credito': Decimal('45.00')
        },
    ]
    
    carreras_creadas = []
    for config in carreras_config:
        carrera, created = Carrera.objects.get_or_create(
            codigo=config['codigo'],
            defaults={
                'nombre': config['nombre'],
                'precio_credito': config['precio_credito']
            }
        )
        if created:
            print(f"  ✅ {carrera.codigo} - {carrera.nombre} (${carrera.precio_credito}/crédito)")
        else:
            print(f"  ⚠️  {carrera.codigo} - Ya existía")
        carreras_creadas.append(carrera)
    
    # 2. CREAR GRUPOS DE DJANGO
    print("\n👥 Creando Grupos de Permisos...")
    
    grupos_nombres = ['Director', 'Coordinador', 'Tesorero', 'Administrativo', 'Profesor', 'Estudiante']
    
    for nombre in grupos_nombres:
        grupo, created = Group.objects.get_or_create(name=nombre)
        if created:
            print(f"  ✅ Grupo '{nombre}' creado")
        else:
            print(f"  ⚠️  Grupo '{nombre}' ya existía")
    
    # RESUMEN
    print("\n" + "=" * 80)
    print("✅ ESTRUCTURA BASE CREADA")
    print("=" * 80)
    print(f"📊 Carreras: {Carrera.objects.count()}")
    print(f"👥 Grupos: {Group.objects.count()}")
    print("\n📌 Siguiente paso: Ejecutar script 2 (crear_malla.py)")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    crear_estructura()