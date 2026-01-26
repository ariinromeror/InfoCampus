from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# --- INFRAESTRUCTURA ACADÉMICA ---

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

# --- USUARIO EXTENDIDO (EL MOTOR DE ROLES) ---

class Usuario(AbstractUser):
    ROLES = (
        ('director', 'Director'),
        ('coordinador', 'Coordinador'),
        ('tesorero', 'Tesorero'), # Añadido para el Punto 4.1
        ('administrativo', 'Administrativo'),
        ('profesor', 'Profesor'),
        ('estudiante', 'Estudiante'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # Flags de Control (Visión 10 años)
    en_mora = models.BooleanField(default=False)
    es_becado = models.BooleanField(default=False)
    porcentaje_beca = models.IntegerField(default=0) # Para el Punto 4.1
    
    foto = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    
    # Seguridad (Punto 2.4)
    dispositivo_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_rol_display()})"

# --- ACADÉMICO ---

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='materias')
    profesor = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'rol': 'profesor'},
        related_name='materias_dictadas'
    )
    # Punto 2.1: El método de asistencia se define por materia
    metodo_asistencia_default = models.CharField(
        max_length=20, 
        choices=(('qr_dinamico', 'QR Dinámico'), ('qr_estatico', 'QR Estático'), ('manual', 'Manual')),
        default='manual'
    )

    def __str__(self):
        return f"{self.nombre} ({self.carrera.codigo})"

# --- CONTROL DE NOTAS Y AUDITORÍA (PUNTO 2.3) ---

class Nota(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notas_academicas', limit_choices_to={'rol': 'estudiante'})
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=4, decimal_places=2)
    
    # Auditoría (Indispensable a 10 años)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='notas_editadas'
    )

    class Meta:
        unique_together = ('estudiante', 'materia') # Un estudiante solo tiene una nota por materia

# --- ASISTENCIA ANTI-FRAUDE (PUNTO 2.4) ---

class Asistencia(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'estudiante'})
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    latitud = models.FloatField(null=True, blank=True) # Para validación GPS futura
    longitud = models.FloatField(null=True, blank=True)
    validado = models.BooleanField(default=True)

    class Meta:
        unique_together = ('estudiante', 'materia', 'fecha')