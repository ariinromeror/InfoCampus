import io
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.contrib import messages
from .models import Materia, Estudiante, RegistroActividad

# Herramientas para el reporte PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ==========================================================
# 1. DASHBOARD / RESUMEN GENERAL
# ==========================================================
@login_required
def dashboard(request):
    conteo_materias = Materia.objects.count()
    conteo_estudiantes = Estudiante.objects.count()
    ultimos_registros = RegistroActividad.objects.all().order_by('-fecha')[:5]
    
    context = {
        'materias_count': conteo_materias,
        'estudiantes_count': conteo_estudiantes,
        'registros': ultimos_registros,
    }
    return render(request, 'portal/dashboard.html', context)

# ==========================================================
# 2. GESTIÓN DE MATERIAS (CRUD)
# ==========================================================
@login_required
def gestion_materias(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        if nombre and codigo:
            Materia.objects.create(nombre=nombre, codigo=codigo)
            messages.success(request, "Materia creada correctamente.")
            return redirect('gestion_materias')

    materias = Materia.objects.all()
    return render(request, 'portal/gestion_materias.html', {'materias': materias})

@login_required
def editar_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        if nombre and codigo:
            materia.nombre = nombre
            materia.codigo = codigo
            materia.save()
            messages.success(request, "Materia actualizada.")
            return redirect('gestion_materias')
    return render(request, 'portal/editar_materia.html', {'materia': materia})

@login_required
def eliminar_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)
    materia.delete()
    messages.warning(request, "Materia eliminada.")
    return redirect('gestion_materias')

# ==========================================================
# 3. GESTIÓN DE ESTUDIANTES (CRUD)
# ==========================================================
@login_required
def gestion_estudiantes(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        cedula_id = request.POST.get('matricula') 
        
        if nombre and email and cedula_id:
            # --- VALIDACIÓN DE SEGURIDAD ---
            # Verificamos si el email ya existe para evitar errores de base de datos
            if Estudiante.objects.filter(email=email).exists():
                messages.error(request, f"El correo {email} ya está registrado.")
                return redirect('gestion_estudiantes')

            # --- LÓGICA DE MATRÍCULA INTELIGENTE ---
            anio_actual = datetime.now().year
            iniciales = "".join([n[0].upper() for n in nombre.split()[:2]])
            ultimos_digitos = str(cedula_id)[-4:]
            codigo_generado = f"{anio_actual}-{iniciales}-{ultimos_digitos}"
            
            # Verificamos si la matrícula generada ya existe (poco probable, pero posible)
            if Estudiante.objects.filter(matricula=codigo_generado).exists():
                messages.error(request, "Ya existe un estudiante con esta matrícula generada.")
                return redirect('gestion_estudiantes')

            # Si todo está bien, creamos
            Estudiante.objects.create(
                nombre=nombre, 
                email=email, 
                matricula=codigo_generado
            )
            messages.success(request, f"Estudiante {nombre} registrado con éxito.")
            return redirect('gestion_estudiantes')
            
    estudiantes = Estudiante.objects.all()
    return render(request, 'portal/gestion_estudiantes.html', {'estudiantes': estudiantes})

# ==========================================================
# 4. PROCESOS ACADÉMICOS (INSCRIPCIÓN Y NOTAS)
# ==========================================================
@login_required
def inscribir_estudiante(request):
    estudiantes = Estudiante.objects.all()
    materias = Materia.objects.all()
    
    if request.method == 'POST':
        est_id = request.POST.get('estudiante')
        mat_id = request.POST.get('materia')
        
        estudiante = get_object_or_404(Estudiante, id=est_id)
        materia = get_object_or_404(Materia, id=mat_id)
        
        # --- VALIDACIÓN DE DUPLICADOS ---
        # Verificamos si ya existe el alumno en esa materia dentro de RegistroActividad
        # buscando el texto en el campo 'valor' o una relación directa
        ya_inscrito = RegistroActividad.objects.filter(
            materia=materia, 
            valor__contains=estudiante.nombre,
            tipo='INSCRIPCION'
        ).exists()

        if ya_inscrito:
            messages.error(request, f"El estudiante {estudiante.nombre} ya está inscrito en {materia.nombre}.")
            return redirect('inscribir_estudiante')

        # Si no está inscrito, procedemos
        RegistroActividad.objects.create(
            materia=materia,
            alumno=request.user, 
            tipo='INSCRIPCION',
            valor=f"Inscrito: {estudiante.nombre}"
        )
        messages.success(request, f"{estudiante.nombre} ha sido inscrito en {materia.nombre}.")
        return redirect('dashboard')

    return render(request, 'portal/inscribir.html', {
        'estudiantes': estudiantes,
        'materias': materias
    })

@login_required
def registrar_actividad(request, materia_id):
    """ Función para registrar notas o asistencia individual """
    materia = get_object_or_404(Materia, id=materia_id)
    estudiantes = Estudiante.objects.all()
    
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        valor = request.POST.get('valor')
        
        RegistroActividad.objects.create(
            materia=materia,
            alumno=request.user, 
            tipo=tipo,
            valor=valor
        )
        messages.success(request, "Actividad registrada correctamente.")
        return redirect('dashboard')

    return render(request, 'portal/registrar_actividad.html', {
        'materia': materia,
        'estudiantes': estudiantes
    })

# ==========================================================
# 5. REPORTES Y EXPORTACIÓN
# ==========================================================
@login_required
def generar_reporte_pdf(request):
    materias = Materia.objects.all()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "INFOCAMPUS - REPORTE DETALLADO")
    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Usuario: {request.user.username}")
    p.line(100, 720, 500, 720)
    
    y = 690
    for materia in materias:
        p.drawString(100, y, f"• {materia.nombre} | Código: {materia.codigo}")
        y -= 20
        
    p.showPage()
    p.save()
    buffer.seek(0)
    
    return FileResponse(buffer, as_attachment=True, filename='Reporte_InfoCampus.pdf')