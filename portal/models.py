from django.db import models
from django.contrib.auth.models import AbstractUser

# --- 1. INFRAESTRUCTURA Y CARRERAS ---
class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

# --- 2. USUARIOS Y CONTROL DE ACCESO (RBAC) ---
class Usuario(AbstractUser):
    ROLES = (
        ('director', 'Director'),
        ('coordinador', 'Coordinador'),
        ('tesorero', 'Tesorero'),
        ('administrativo', 'Administrativo'),
        ('profesor', 'Profesor'),
        ('estudiante', 'Estudiante'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # Lógica de Negocio
    en_mora = models.BooleanField(default=False)
    es_becado = models.BooleanField(default=False)
    porcentaje_beca = models.IntegerField(default=0)
    
    carrera = models.ForeignKey(
        Carrera, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='usuarios'
    )

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"

# --- 3. MALLA CURRICULAR Y MATERIAS ---
class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    carrera = models.ForeignKey(
        Carrera, 
        on_delete=models.CASCADE, 
        related_name='materias'
    )
    nivel = models.IntegerField(default=1)  # Del 1 al 10
    
    prerrequisito = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='sucesores'
    )

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} - Nivel {self.nivel}"

# --- 4. GESTIÓN ACADÉMICA E HISTORIAL ---
class CargaAcademica(models.Model):
    DIAS = (
        ('LU', 'Lunes'), ('MA', 'Martes'), ('MI', 'Miércoles'),
        ('JU', 'Jueves'), ('VI', 'Viernes'), ('SA', 'Sábado')
    )

    # El Estudiante es el centro de esta tabla para el historial
    estudiante = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'estudiante'},
        related_name='inscripciones',
        null=True, blank=True
    )
    
    # El Profesor que dicta (opcional en historial)
    profesor = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'profesor'},
        related_name='cargas_docentes',
        null=True, blank=True
    )
    
    materia = models.ForeignKey(
        Materia, 
        on_delete=models.CASCADE, 
        related_name='asignaciones'
    )
    
    # Datos de la cursada
    seccion = models.CharField(max_length=10, default='A')
    aula = models.CharField(max_length=50, blank=True, null=True)
    dia = models.CharField(max_length=2, choices=DIAS, default='LU')
    hora_inicio = models.TimeField(null=True, blank=True)
    
    # Datos del Periodo y Rendimiento
    periodo_lectivo = models.CharField(max_length=20, default='2026-01')
    nota_final = models.FloatField(default=0.0) # Escala 0 a 10
    pagado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Cargas Académicas"

    def __str__(self):
        nombre_est = self.estudiante.username if self.estudiante else "Sin asignar"
        return f"{nombre_est} - {self.materia.nombre} ({self.periodo_lectivo})"