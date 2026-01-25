from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('director', 'Director (SuperAdmin)'),
        ('coordinador', 'Coordinador Académico'),
        ('administrativo', 'Administrativo/Tesorería'),
        ('secretaria', 'Secretaría/Admisiones'),
        ('profesor', 'Profesor'),
        ('estudiante', 'Estudiante'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')

    groups = models.ManyToManyField('auth.Group', related_name='portal_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='portal_user_permissions', blank=True)

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self): return self.nombre

class Profesor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'profesor'})
    especialidad = models.CharField(max_length=100)
    def __str__(self): return self.usuario.username

class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'estudiante'})
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True)
    def __str__(self): return self.usuario.username

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True)
    def __str__(self): return self.nombre