import io
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.contrib import messages
from .models import Materia, Estudiante, RegistroActividad
from django.db.models import Q

# Herramientas para el reporte PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ==========================================================
# 1. DASHBOARD
# ==========================================================
@login_required
def dashboard(request):
    """ Resumen general y logs para el usuario autenticado """
    context = {
        'materias_count': Materia.objects.count(),
        'estudiantes_count': Estudiante.objects.count(),
        'registros': RegistroActividad.objects.all().order_by('-id')[:8],
    }
    return render(request, 'portal/dashboard.html', context)

# ==========================================================
# 2. GESTIÓN ACADÉMICA (MATERIAS)
# ==========================================================
@login_required
def gestion_materias(request):
    if request.user.perfil.rol not in ['admin', 'administrativo']:
        messages.error(request, "No tienes permisos para gestionar materias.")
        return redirect('dashboard')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        if nombre and codigo:
            materia = Materia.objects.create(nombre=nombre, codigo=codigo)
            RegistroActividad.objects.create(
                usuario_registro=request.user,
                materia=materia,
                tipo="extra",
                valor=f"Materia Creada: {nombre}"
            )
            messages.success(request, "Materia creada correctamente.")
            return redirect('gestion_materias')

    materias = Materia.objects.all().order_by('nombre')
    return render(request, 'portal/gestion_materias.html', {'materias': materias})

@login_required
def editar_materia(request, materia_id):
    """ Función para modificar datos de una materia existente """
    if request.user.perfil.rol not in ['admin', 'administrativo']:
        messages.error(request, "No tienes permiso para editar.")
        return redirect('dashboard')

    materia = get_object_or_404(Materia, id=materia_id)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        if nombre and codigo:
            materia.nombre = nombre
            materia.codigo = codigo
            materia.save()
            messages.success(request, f"Materia {nombre} actualizada.")
            return redirect('gestion_materias')
            
    return render(request, 'portal/editar_materia.html', {'materia': materia})

@login_required
def eliminar_materia(request, materia_id):
    if request.user.perfil.rol != 'admin':
        messages.error(request, "Solo el administrador puede eliminar materias.")
        return redirect('gestion_materias')

    materia = get_object_or_404(Materia, id=materia_id)
    RegistroActividad.objects.create(
        usuario_registro=request.user,
        tipo="extra",
        valor=f"Eliminó materia: {materia.nombre}"
    )
    materia.delete()
    messages.warning(request, "Materia eliminada.")
    return redirect('gestion_materias')

# ==========================================================
# 3. GESTIÓN DE ESTUDIANTES
# ==========================================================
@login_required
def gestion_estudiantes(request):
    if request.user.perfil.rol not in ['admin', 'administrativo']:
        return redirect('dashboard')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        cedula = request.POST.get('matricula') 
        
        if nombre and email and cedula:
            anio = datetime.now().year
            iniciales = "".join([n[0].upper() for n in nombre.strip().split()[:2]])
            ultimos_4 = str(cedula).strip()[-4:]
            codigo = f"{anio}-{iniciales}-{ultimos_4}"

            estudiante = Estudiante.objects.create(nombre=nombre, email=email, matricula=codigo)
            
            RegistroActividad.objects.create(
                usuario_registro=request.user,
                estudiante=estudiante,
                tipo="extra",
                valor=f"Ingreso: {codigo}"
            )
            messages.success(request, f"Estudiante {nombre} registrado.")
            return redirect('gestion_estudiantes')
            
    return render(request, 'portal/gestion_estudiantes.html', {
        'estudiantes': Estudiante.objects.all().order_by('-id')
    })

@login_required
def eliminar_estudiante(request, estudiante_id):
    if request.user.perfil.rol not in ['admin', 'administrativo']:
        messages.error(request, "No tienes permiso para eliminar estudiantes.")
        return redirect('dashboard')
        
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    nombre_e = estudiante.nombre
    
    RegistroActividad.objects.create(
        usuario_registro=request.user,
        tipo="extra",
        valor=f"Eliminó al estudiante: {nombre_e}"
    )
    
    estudiante.delete()
    messages.warning(request, f"Estudiante {nombre_e} eliminado.")
    return redirect('gestion_estudiantes')

# ==========================================================
# 4. PROCESOS ACADÉMICOS (NOTAS E INSCRIPCIÓN)
# ==========================================================
@login_required
def inscribir_estudiante(request):
    if request.user.perfil.rol not in ['admin', 'administrativo']:
        return redirect('dashboard')

    if request.method == 'POST':
        est_id = request.POST.get('estudiante')
        mat_id = request.POST.get('materia')
        
        estudiante = get_object_or_404(Estudiante, id=est_id)
        materia = get_object_or_404(Materia, id=mat_id)
        
        try:
            RegistroActividad.objects.create(
                usuario_registro=request.user, 
                estudiante=estudiante,
                materia=materia,
                tipo='INSCRIPCION',
                valor="Inscripción Confirmada"
            )
            materia.estudiantes_inscritos.add(estudiante)
            messages.success(request, f"Inscripción exitosa: {estudiante.nombre}")
            return redirect('dashboard')
        except Exception: 
            messages.warning(request, f"El estudiante {estudiante.nombre} ya está en esa materia.")
            return redirect('inscribir_estudiante')

    return render(request, 'portal/inscribir.html', {
        'estudiantes': Estudiante.objects.all().order_by('nombre'),
        'materias': Materia.objects.all().order_by('nombre')
    })

@login_required
def registrar_nota(request):
    if request.user.perfil.rol not in ['admin', 'profesor']:
        messages.error(request, "No tienes permiso para calificar.")
        return redirect('dashboard')

    if request.method == 'POST':
        est_id = request.POST.get('estudiante')
        mat_id = request.POST.get('materia')
        nota_valor = request.POST.get('nota')

        estudiante = get_object_or_404(Estudiante, id=est_id)
        materia = get_object_or_404(Materia, id=mat_id)

        RegistroActividad.objects.create(
            usuario_registro=request.user,
            estudiante=estudiante,
            materia=materia,
            tipo='nota',
            valor=f"Calificación: {nota_valor}"
        )
        messages.success(request, f"Nota registrada para {estudiante.nombre}")
        return redirect('dashboard')

    return render(request, 'portal/registrar_nota.html', {
        'estudiantes': Estudiante.objects.all(),
        'materias': Materia.objects.all()
    })

# ==========================================================
# 5. REPORTES
# ==========================================================
@login_required
def generar_reporte_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "INFOCAMPUS - REPORTE GENERAL")
    y = 700
    for m in Materia.objects.all():
        p.drawString(100, y, f"- {m.nombre} ({m.codigo})")
        y -= 20
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Reporte_Campus.pdf')