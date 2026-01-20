from django.db import models
from django.contrib.auth.models import User

# ==========================================================
# 1. PERFILES Y SEGURIDAD (Jerarquía de Usuarios)
# ==========================================================
class Perfil(models.Model):
    """
    Extiende la información de User para manejar los 4 niveles de acceso.
    """
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
# 2. DIRECTORIO MAESTRO (Entidades Independientes)
# ==========================================================
class Estudiante(models.Model):
    """
    Base de datos de alumnos. 
    Aquí se almacenan los datos personales y la matrícula generada.
    """
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
# 3. GESTIÓN ACADÉMICA (Materias y Relaciones)
# ==========================================================
class Materia(models.Model):
    """
    Catálogo de materias. 
    Relaciona a los Estudiantes con los Profesores (User).
    """
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=15, unique=True)
    
    # El profesor es un usuario del sistema
    profesor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='materias_asignadas'
    )
    
    # Estudiantes inscritos desde el directorio maestro
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
# 4. TRANSACCIONES Y NOTAS (Historial de Actividad)
# ==========================================================
class RegistroActividad(models.Model):
    """
    Registra cada evento: Inscripciones, Notas y Asistencias.
    """
    TIPOS = (
        ('nota', 'Nota'), 
        ('asistencia', 'Asistencia'), 
        ('extra', 'Extra'),
        ('INSCRIPCION', 'Inscripción')
    )
    
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='registros')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='actividades')
    
    # Quién realizó el registro (Admin, Profe o Administrativo)
    usuario_registro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    tipo = models.CharField(max_length=15, choices=TIPOS)
    valor = models.CharField(max_length=50) # Espacio suficiente para notas o comentarios
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de Actividad"
        verbose_name_plural = "Registros de Actividades"
        ordering = ['-fecha'] # El más reciente primero

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.estudiante.nombre} en {self.materia.nombre}"