import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portal.models import Usuario, Carrera, Materia, Nota

def generar_datos():
    print("--- 🚀 Iniciando siembra (Versión Rápida) ---")

    # 1. Carreras
    for nom, cod in [("Software", "SOFT"), ("Admin", "ADM")]:
        Carrera.objects.get_or_create(nombre=nom, codigo=cod)
    
    carreras = Carrera.objects.all()
    print(f"✅ Carreras listas.")

    # 2. Profesores
    profes = []
    for i in range(1, 4):
        p, _ = Usuario.objects.get_or_create(
            username=f"profe{i}", 
            defaults={'rol': 'profesor', 'first_name': f"Prof {i}"}
        )
        p.set_password("profe123")
        p.save()
        profes.append(p)
    print(f"✅ Profesores listos.")

    # 3. Materias
    mats = []
    for m_nom in ["Programación", "Base de Datos", "Contabilidad"]:
        mat, _ = Materia.objects.get_or_create(
            nombre=m_nom, 
            carrera=random.choice(carreras),
            defaults={'profesor': random.choice(profes)}
        )
        mats.append(mat)
    print(f"✅ Materias listas.")

    # 4. Estudiantes (Bajamos a 30 para probar velocidad)
    print("⏳ Creando estudiantes y notas... espera un momento.")
    for i in range(1, 31):
        est, _ = Usuario.objects.get_or_create(
            username=f"estudiante{i}",
            defaults={'rol': 'estudiante', 'en_mora': random.choice([True, False, False])}
        )
        est.set_password("est123")
        est.save()
        
        # Nota rápida
        Nota.objects.get_or_create(estudiante=est, materia=random.choice(mats), defaults={'valor': 8.5})

    print(f"--- ✨ ÉXITO TOTAL: Sistema cargado ---")

if __name__ == "__main__":
    generar_datos()