from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Carrera, Profesor, Estudiante, Materia

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Roles', {'fields': ('rol',)}),)
    list_display = ('username', 'email', 'rol', 'is_staff')

admin.site.register(Carrera)
admin.site.register(Profesor)
admin.site.register(Estudiante)
admin.site.register(Materia)