import os
import django

# 1. Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portal.models import Usuario
from django.core import mail

def crear_datos_prueba():
    print("🚀 Iniciando creación de usuarios profesionales...")
    
    # Lista de usuarios: (username, password, rol, email)
    usuarios_test = [
        ('director_boss', 'admin123', 'director', 'director@academia.com'),
        ('coord_acad', 'coord123', 'coordinador', 'coordinacion@academia.com'),
        ('tesorero_fin', 'teso123', 'administrativo', 'finanzas@academia.com'),
        ('secre_adm', 'secre123', 'secretaria', 'admisiones@academia.com'),
        ('profe_test', 'profe123', 'profesor', 'profesor@gmail.com'),
        ('alumno_test', 'alumno123', 'estudiante', 'estudiante@gmail.com'),
    ]

    for username, password, rol, email in usuarios_test:
        if not Usuario.objects.filter(username=username).exists():
            # Creamos el usuario en la base de datos
            Usuario.objects.create_user(
                username=username, 
                password=password, 
                rol=rol,
                email=email
            )
            
            # Esto generará el archivo .txt en la carpeta que configuramos en settings.py
            mail.send_mail(
                'Bienvenido al Sistema Académico',
                f'Hola {username}, tu cuenta como {rol} ha sido creada.\nUsuario: {username}\nClave: {password}',
                'sistema@academia.com',
                [email],
                fail_silently=False,
            )
            print(f"✅ Usuario creado: {username} ({rol})")
        else:
            print(f"⚠️ El usuario {username} ya existe.")

    print("\n✨ Proceso terminado. ¡Busca los archivos .txt en tu proyecto!")

if __name__ == '__main__':
    crear_datos_prueba()