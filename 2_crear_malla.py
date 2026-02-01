"""

SCRIPT 2: Crear Malla Curricular Completa

210 materias (5 carreras × 6 semestres × 7 materias)

Con créditos aleatorios y prerequisitos reales

"""



import os

import django

import random



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()



from portal.models import Carrera, Materia



def crear_malla_curricular():

    print("\n" + "=" * 80)

    print("SCRIPT 2: CREANDO MALLA CURRICULAR")

    print("=" * 80 + "\n")

    

    carreras = Carrera.objects.all()

    

    if not carreras.exists():

        print("❌ ERROR: No hay carreras creadas. Ejecuta primero el script 1.")

        return

    

    # Templates de nombres de materias por tipo

    nombres_base = {

        'matematicas': ['Matemáticas', 'Cálculo', 'Álgebra', 'Estadística', 'Geometría'],

        'ciencias': ['Física', 'Química', 'Biología', 'Ciencias Naturales'],

        'humanidades': ['Filosofía', 'Ética', 'Historia', 'Literatura', 'Arte'],

        'tecnologia': ['Informática', 'Programación', 'Sistemas', 'Redes', 'Base de Datos'],

        'negocios': ['Economía', 'Contabilidad', 'Marketing', 'Finanzas', 'Recursos Humanos'],

        'salud': ['Anatomía', 'Fisiología', 'Farmacología', 'Patología', 'Epidemiología'],

        'derecho': ['Derecho Civil', 'Derecho Penal', 'Derecho Laboral', 'Derecho Constitucional'],

        'psicologia': ['Psicología General', 'Psicología Social', 'Neuropsicología', 'Psicoanálisis'],

    }

    

    # Mapeo de categorías por carrera

    categorias_por_carrera = {

        'ADM': ['matematicas', 'negocios', 'humanidades', 'tecnologia'],

        'ING': ['matematicas', 'ciencias', 'tecnologia'],

        'MED': ['ciencias', 'salud', 'humanidades'],

        'DER': ['derecho', 'humanidades', 'ciencias'],

        'PSI': ['psicologia', 'ciencias', 'humanidades'],

    }

    

    total_materias = 0

    materias_por_carrera = {}

    

    for carrera in carreras:

        print(f"\n📚 Creando malla para {carrera.nombre} ({carrera.codigo})...")

        materias_carrera = []

        categorias = categorias_por_carrera.get(carrera.codigo, ['matematicas', 'ciencias', 'humanidades'])

        

        for semestre in range(1, 7):  # 6 semestres

            print(f"   Semestre {semestre}...", end=" ")

            materias_semestre = []

            

            for num_materia in range(1, 8):  # 7 materias por semestre

                # Seleccionar categoría aleatoria

                categoria = random.choice(categorias)

                nombre_base = random.choice(nombres_base[categoria])

                

                # Generar nombre único

                nombre = f"{nombre_base} {semestre}"

                codigo = f"{carrera.codigo}-{semestre}{num_materia}"

                

                # Créditos aleatorios (2-4)

                creditos = random.choice([2, 3, 3, 4, 4])  # Más probable 3-4

                

                # Crear materia sin prerequisito primero

                materia = Materia.objects.create(

                    nombre=nombre,

                    codigo=codigo,

                    carrera=carrera,

                    semestre=semestre,      # ✅ CORREGIDO: de 'nivel' a 'semestre'

                    creditos=creditos,

                    prerequisito=None       # ✅ CORREGIDO: de 'prerrequisito' a 'prerequisito'

                )

                

                materias_semestre.append(materia)

                total_materias += 1

            

            materias_carrera.extend(materias_semestre)

            print(f"✅ {len(materias_semestre)} materias creadas")

        

        # Asignar prerequisitos (materias del semestre anterior)

        print(f"   Asignando prerequisitos...")

        for semestre in range(2, 7):  # Del semestre 2 al 6

            # ✅ CORREGIDO: de 'nivel' a 'semestre'

            materias_actuales = [m for m in materias_carrera if m.semestre == semestre]

            materias_previas = [m for m in materias_carrera if m.semestre == semestre - 1]

            

            for i, materia in enumerate(materias_actuales):

                # Asignar prerequisito de materia similar del semestre anterior

                if materias_previas:

                    # ✅ CORREGIDO: de 'prerrequisito' a 'prerequisito'

                    prerequisito_obj = materias_previas[i % len(materias_previas)]

                    materia.prerequisito = prerequisito_obj

                    materia.save()

        

        materias_por_carrera[carrera.codigo] = len(materias_carrera)

        print(f"   ✅ Total para {carrera.codigo}: {len(materias_carrera)} materias\n")

    

    # RESUMEN FINAL

    print("=" * 80)

    print("✅ MALLA CURRICULAR CREADA")

    print("=" * 80)

    print(f"📊 Total de materias: {total_materias}")

    print(f"\nDistribución por carrera:")

    for codigo, cantidad in materias_por_carrera.items():

        print(f"   {codigo}: {cantidad} materias (6 semestres × 7 materias)")

    

    # Verificar prerequisitos

    # ✅ CORREGIDO: de 'prerrequisito' a 'prerequisito'

    con_prereq = Materia.objects.exclude(prerequisito__isnull=True).count()

    sin_prereq = Materia.objects.filter(prerequisito__isnull=True).count()

    print(f"\n📌 Prerequisitos:")

    print(f"   Con prerequisito: {con_prereq}")

    print(f"   Sin prerequisito: {sin_prereq} (primer semestre)")

    

    print("\n📌 Siguiente paso: Ejecutar script 3 (crear_usuarios.py)")

    print("=" * 80 + "\n")



if __name__ == '__main__':

    crear_malla_curricular()