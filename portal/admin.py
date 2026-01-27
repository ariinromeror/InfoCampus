from django.contrib import admin
from .models import Usuario, Carrera, Materia, CargaAcademica

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Columnas organizadas para visualización rápida de 300+ alumnos
    list_display = ('dni', 'username', 'rol', 'carrera', 'en_mora', 'es_becado')
    
    # Filtros laterales potentes: Primero por Rol para separar Personal de Alumnos
    # Luego por Carrera y por situación financiera (Mora/Beca)
    list_filter = ('rol', 'carrera', 'en_mora', 'es_becado')
    
    # Búsqueda por DNI y Nombre
    search_fields = ('dni', 'username', 'email')
    
    # Orden predeterminado por carrera para agrupar alumnos
    ordering = ('carrera', 'username')

    # Agrupamos los campos dentro del formulario de edición
    fieldsets = (
        ('Información Personal', {
            'fields': ('username', 'email', 'password', 'dni')
        }),
        ('Rol y Academia', {
            'fields': ('rol', 'carrera', 'is_staff', 'is_superuser', 'groups')
        }),
        ('Situación Financiera', {
            'fields': ('en_mora', 'es_becado', 'porcentaje_beca')
        }),
    )

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('nombre', 'codigo')
    ordering = ('nombre',)

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'carrera', 'nivel', 'prerrequisito')
    list_filter = ('carrera', 'nivel')
    search_fields = ('nombre', 'codigo')
    ordering = ('carrera', 'nivel', 'codigo')

@admin.register(CargaAcademica)
class CargaAcademicaAdmin(admin.ModelAdmin):
    # CORRECCIÓN: Se cambiaron 'periodo' por 'periodo_lectivo' y 'pagado' por 'pagado' (verificar en models)
    # Según tu último models.py, los campos son: 'periodo_lectivo', 'nota_final', 'pagado'
    list_display = ('estudiante', 'materia', 'periodo_lectivo', 'nota_final', 'pagado')
    
    # Filtros ajustados a los nuevos nombres del modelo
    list_filter = ('periodo_lectivo', 'pagado', 'materia__carrera')
    
    # Búsqueda por nombre de alumno (vía relación foreign key) o materia
    search_fields = ('estudiante__username', 'estudiante__dni', 'materia__nombre')
    
    # Orden ascendente por periodo y luego estudiante
    ordering = ('-periodo_lectivo', 'estudiante')

admin.site.site_header = "INFO-CAMPUS: Sistema de Gestión Académica"
admin.site.index_title = "Panel de Control Administrativo"
admin.site.site_title = "Administración Instituto"