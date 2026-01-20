from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    ROLES = (('profesor', 'Profesor'), ('alumno', 'Alumno'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROLES)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    profesor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='materias_profe')
    alumnos = models.ManyToManyField(User, related_name='materias_alumno', blank=True)

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"

    def __str__(self):
        return self.nombre

class RegistroActividad(models.Model):
    TIPOS = (('nota', 'Nota'), ('asistencia', 'Asistencia'), ('extra', 'Extra'))
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15, choices=TIPOS)
    valor = models.CharField(max_length=10)
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de Actividad"
        verbose_name_plural = "Registros de Actividades"