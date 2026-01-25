import os
from pathlib import Path
import environ

# 1. Inicializar environ para manejo de variables de entorno
env = environ.Env(
    DEBUG=(bool, False)
)

# 2. Definir la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# 3. Leer el archivo .env (La Bóveda)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# --- CONFIGURACIÓN DE SEGURIDAD (Desde .env) ---
# Si no encuentra la llave en el .env, usará la de respaldo por seguridad
SECRET_KEY = env('SECRET_KEY', default='django-insecure-cambiar-por-env-key')
DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS = []

# --- APLICACIONES ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Librerías Externas
    'corsheaders', 
    
    # Tus Aplicaciones
    'portal', 
]

# Modelo de usuario personalizado (Clave para tu sistema multi-rol)
AUTH_USER_MODEL = 'portal.Usuario'

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Debe ir arriba para CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# --- SEGURIDAD Y CORS (Comunicación con React) ---
CORS_ALLOW_ALL_ORIGINS = True 

# --- PLANTILLAS ---
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

# --- BASE DE DATOS (Relacional SQLite) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- LOCALIZACIÓN ---
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- ARCHIVOS ESTÁTICOS ---
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- SISTEMA DE CORREOS (Logs locales para pruebas) ---
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'mensajes_sistema')