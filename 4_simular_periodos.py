"""
SCRIPT 4: Simulación de Ciclo de Vida Académico (2025-02 y 2026-01)
Este script actúa como el motor de reglas del sistema:
1. Crea los periodos lectivos.
2. Simula el Semestre 1 (2025-02) con aprobaciones y reprobaciones.
3. Simula el Semestre 2 (2026-01) aplicando validación estricta de prerequisitos.
"""

import os
import django
import random
from datetime import date, time
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portal.models import Usuario, Carrera, Materia, PeriodoLectivo, Seccion, Inscripcion, Pago

# Configuración de simulación
DURACION_HORA = 2 # Horas por clase
PROBABILIDAD_APROBAR = 0.75 # 75% de probabilidad de aprobar
TASAS_PAGO = 0.80 # 80% de los estudiantes pagan sus materias

def log(msg):
    print(f" {msg}")

def ejecutar_simulacion():
    print("\n" + "=" * 80)
    print("🚀 SCRIPT 4: SIMULACIÓN DE CICLO ACADÉMICO PROFESIONAL")
    print("=" * 80 + "\n")

    # 1. PREPARACIÓN DE PERIODOS
    p2025_02, _ = PeriodoLectivo.objects.get_or_create(
        codigo="2025-02",
        defaults={
            "nombre": "Segundo Semestre 2025",
            "fecha_inicio": date(2025, 8, 1),
            "fecha_fin": date(2025, 12, 15),
            "activo": False
        }
    )
    
    p2026_01, _ = PeriodoLectivo.objects.get_or_create(
        codigo="2026-01",
        defaults={
            "nombre": "Primer Semestre 2026",
            "fecha_inicio": date(2026, 1, 20),
            "fecha_fin": date(2026, 6, 10),
            "activo": True
        }
    )

    estudiantes = Usuario.objects.filter(rol='estudiante')
    profesores = list(Usuario.objects.filter(rol='profesor'))

    if not estudiantes.exists() or not profesores:
        print("❌ ERROR: Faltan estudiantes o profesores. Ejecuta los scripts previos.")
        return

    # =========================================================================
    # FASE 1: SEMESTRE 2025-02 (Inscripción inicial en Semestre 1)
    # =========================================================================
    print(f"📅 SIMULANDO PERIODO {p2025_02.codigo} (Semestre Base)...")
    
    for estudiante in estudiantes:
        # Buscamos las materias del 1er semestre de su carrera
        materias_primer_sem = Materia.objects.filter(carrera=estudiante.carrera, semestre=1)
        
        for materia in materias_primer_sem:
            # 1. Crear o buscar sección para la materia
            seccion, _ = Seccion.objects.get_or_create(
                materia=materia,
                periodo=p2025_02,
                codigo_seccion="A",
                defaults={
                    "profesor": random.choice(profesores),
                    "dia": random.choice(['LU', 'MA', 'MI', 'JU', 'VI']),
                    "hora_inicio": time(8, 0),
                    "hora_fin": time(10, 0),
                    "aula": f"A-{random.randint(100, 300)}",
                    "cupo_maximo": 40
                }
            )

            # 2. Inscribir al alumno
            insc, creada = Inscripcion.objects.get_or_create(
                estudiante=estudiante,
                seccion=seccion,
                defaults={"estado": "inscrito"}
            )

            if creada:
                # 3. Asignar nota y estado final del semestre pasado
                nota = Decimal(random.uniform(4.0, 10.0)).quantize(Decimal('0.00'))
                insc.nota_final = nota
                insc.estado = "aprobado" if nota >= 7.0 else "reprobado"
                insc.save()

                # 4. Simular Pago (Para que no todos deban dinero)
                if random.random() < TASAS_PAGO:
                    costo = Decimal(materia.creditos) * estudiante.carrera.precio_credito
                    if estudiante.es_becado:
                        costo -= costo * (Decimal(estudiante.porcentaje_beca) / 100)
                    
                    Pago.objects.create(
                        inscripcion=insc,
                        monto=costo,
                        metodo_pago='transferencia',
                        procesado_por=Usuario.objects.filter(rol='tesorero').first()
                    )

    log(f"✅ Periodo 2025-02 completado con éxito.")

    # =========================================================================
    # FASE 2: SEMESTRE 2026-01 (Inscripción con Lógica de Prerequisitos)
    # =========================================================================
    print(f"\n📅 SIMULANDO PERIODO {p2026_01.codigo} (Lógica de Malla Curricular)...")
    
    stats_aprobados = 0
    stats_bloqueados = 0

    for estudiante in estudiantes:
        # Intentamos inscribirlo en materias del 2do Semestre
        materias_segundo_sem = Materia.objects.filter(carrera=estudiante.carrera, semestre=2)
        
        for materia in materias_segundo_sem:
            # --- LÓGICA DE PREREQUISITO (La Biblia del Senior) ---
            requisito = materia.prerequisito
            esta_apto = True
            
            if requisito:
                # Verificamos si el alumno tiene la materia previa aprobada en el periodo anterior
                aprobada = Inscripcion.objects.filter(
                    estudiante=estudiante,
                    seccion__materia=requisito,
                    estado='aprobado'
                ).exists()
                
                if not aprobada:
                    esta_apto = False
            
            if esta_apto:
                # Crear sección para el nuevo periodo
                seccion, _ = Seccion.objects.get_or_create(
                    materia=materia,
                    periodo=p2026_01,
                    codigo_seccion="A",
                    defaults={
                        "profesor": random.choice(profesores),
                        "dia": random.choice(['LU', 'MA', 'MI', 'JU', 'VI']),
                        "hora_inicio": time(10, 0),
                        "hora_fin": time(12, 0),
                        "aula": f"B-{random.randint(100, 300)}",
                        "cupo_maximo": 40
                    }
                )
                Inscripcion.objects.get_or_create(estudiante=estudiante, seccion=seccion)
                stats_aprobados += 1
            else:
                # RECURSAMIENTO: El alumno debe repetir la materia reprobada en lugar de avanzar
                materia_reprobada = requisito
                seccion_repeticion, _ = Seccion.objects.get_or_create(
                    materia=materia_reprobada,
                    periodo=p2026_01,
                    codigo_seccion="REP",
                    defaults={
                        "profesor": random.choice(profesores),
                        "dia": "SA", # Clases de repetición los Sábados
                        "hora_inicio": time(8, 0),
                        "hora_fin": time(11, 0),
                        "aula": "LAB-1",
                        "cupo_maximo": 20
                    }
                )
                Inscripcion.objects.get_or_create(estudiante=estudiante, seccion=seccion_repeticion)
                stats_bloqueados += 1

    # =========================================================================
    # RESUMEN FINAL
    # =========================================================================
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE LA SIMULACIÓN")
    print("=" * 80)
    print(f"📖 Materias de nivel superior inscritas: {stats_aprobados}")
    print(f"⚠️ Alumnos bloqueados (Enviados a recursamiento): {stats_bloqueados}")
    print(f"💰 Total de transacciones simuladas: {Pago.objects.count()}")
    print("-" * 80)
    print("✅ Sistema listo para pruebas de Dashboard y Estado de Cuenta.")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    ejecutar_simulacion()