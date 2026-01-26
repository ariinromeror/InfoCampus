from django.contrib import admin
from .models import Usuario, Carrera, Materia, Nota

# Registramos los modelos para que aparezcan en el panel de administrador
admin.site.register(Usuario)
admin.site.register(Carrera)
admin.site.register(Materia)
admin.site.register(Nota)