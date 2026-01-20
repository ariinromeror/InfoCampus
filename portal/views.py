from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Materia, RegistroActividad

@login_required
def dashboard(request):
    # Datos para los indicadores del dashboard
    conteo_materias = Materia.objects.count()
    ultimos_registros = RegistroActividad.objects.all().order_by('-fecha')[:5]
    
    context = {
        'materias_count': conteo_materias,
        'registros': ultimos_registros,
    }
    return render(request, 'portal/dashboard.html', context)

@login_required
def gestion_materias(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        
        if nombre and codigo:
            # Creamos la materia
            nueva_materia = Materia.objects.create(nombre=nombre, codigo=codigo)
            
            # REGISTRO SENIOR: Guardamos la actividad automáticamente
            RegistroActividad.objects.create(
                usuario=request.user,
                accion=f"Creó la materia: {nombre} ({codigo})"
            )
            
            return redirect('gestion_materias')

    materias = Materia.objects.all()
    return render(request, 'portal/gestion_materias.html', {'materias': materias})
def eliminar_materia(request, materia_id):
    # Buscamos la materia por su ID único
    materia = Materia.objects.get(id=materia_id)
    materia.delete()
    # Volvemos a la página de gestión automáticamente
    return redirect('gestion_materias')