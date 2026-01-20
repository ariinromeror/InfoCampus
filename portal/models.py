from django.db import models
from django.contrib.auth.models import User

# ==========================================================
# 1. PERFILES Y SEGURIDAD
# ==========================================================
class Perfil(models.Model):
    ROLES = (
        ('admin', 'Administrador'),
        ('administrativo', 'Personal Administrativo'),
        ('profesor', 'Profesor'),
        ('estudiante', 'Estudiante'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"


# ==========================================================
# 2. DIRECTORIO MAESTRO
# ==========================================================
class Estudiante(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=25, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self):
        return f"{self.nombre} ({self.matricula})"


# ==========================================================
# 3. GESTIÓN ACADÉMICA
# ==========================================================
class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=15, unique=True)
    profesor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='materias_asignadas'
    )
    # Mantenemos esto para consultas rápidas, pero lo gestionaremos desde la vista
    estudiantes_inscritos = models.ManyToManyField(
        Estudiante, 
        related_name='materias', 
        blank=True
    )

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


# ==========================================================
# 4. TRANSACCIONES (EL CORAZÓN DEL SISTEMA)
# ==========================================================
class RegistroActividad(models.Model):
    TIPOS = (
        ('nota', 'Nota'), 
        ('asistencia', 'Asistencia'), 
        ('extra', 'Extra'),
        ('INSCRIPCION', 'Inscripción')
    )
    
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='registros')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='actividades')
    usuario_registro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tipo = models.CharField(max_length=15, choices=TIPOS)
    valor = models.CharField(max_length=50) 
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de Actividad"
        verbose_name_plural = "Registros de Actividades"
        ordering = ['-fecha']
        
        # --- CIMIENTOS: REGLA DE ORO ---
        # Impide físicamente que un estudiante se inscriba 2 veces en la misma materia
        constraints = [
            models.UniqueConstraint(
                fields=['estudiante', 'materia', 'tipo'], 
                name='unique_inscripcion_estudiante',
                condition=models.Q(tipo='INSCRIPCION')
            )
        ]

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.estudiante.nombre} en {self.materia.nombre}"