import os
from pathlib import Path
from dotenv import load_dotenv # Importación necesaria para el Punto 1.1

# 1. CARGA DE BÓVEDA
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. SEGURIDAD (Desde .env)
SECRET_KEY = os.getenv('SECRET_KEY', 'clave-de-emergencia-por-si-falla-el-env')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

# 3. APLICACIONES
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Librerías externas
    'rest_framework',
    'corsheaders', 
    # Tu aplicación
    'portal',
]

# 4. MIDDLEWARE (CorsMiddleware siempre arriba)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 5. BASE DE DATOS (Preparada para el Punto 1.2)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / os.getenv('DB_NAME', 'db.sqlite3'),
    }
}

# 6. MODELO DE USUARIO PERSONALIZADO
AUTH_USER_MODEL = 'portal.Usuario'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 7. INTERNACIONALIZACIÓN (Configurado para tu región)
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Caracas' # Ajusta esto a tu zona horaria para los Logs de 10 años
USE_I18N = True
USE_TZ = True

# 8. ARCHIVOS ESTÁTICOS Y MEDIA
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 9. CONFIGURACIÓN DE CORS (Conexión segura con React)
CORS_ALLOW_ALL_ORIGINS = True 
CORS_ALLOW_CREDENTIALS = True

# 10. DJANGO REST FRAMEWORK (Configuración de acceso inicial)
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', # Cambiaremos a IsAuthenticated en el Punto 1.3
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}