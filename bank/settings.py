from pathlib import Path
import os
import dj_database_url

# ----------------------------
# BASE & SECRET
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "fallback-secret-key")
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

# ----------------------------
# HOSTS & URL SLASH FIX
# ----------------------------
ALLOWED_HOSTS = [
    ".vercel.app",
    "localhost",
    "127.0.0.1",
]

# Disable automatic trailing slash redirect to prevent CORS preflight redirect
APPEND_SLASH = False

# ----------------------------
# INSTALLED APPS
# ----------------------------
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',  # static files
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # CORS
    'rest_framework',
    'rest_framework_simplejwt',  # JWT auth
    'login_create',
    'transection',
    'banking_system',
]

# ----------------------------
# MIDDLEWARE
# ----------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # MUST be first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------------
# ROOT URLS & WSGI
# ----------------------------
ROOT_URLCONF = 'bank.urls'
WSGI_APPLICATION = 'bank.wsgi.application'

# ----------------------------
# AUTH
# ----------------------------
AUTH_USER_MODEL = 'login_create.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# ----------------------------
# REST FRAMEWORK
# ----------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# ----------------------------
# CORS SETTINGS
# ----------------------------
CORS_ALLOW_ALL_ORIGINS = True  # For dev
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'accept',
    'origin',
    'x-csrftoken',
]
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

# ----------------------------
# TEMPLATES
# ----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ----------------------------
# DATABASE
# ----------------------------
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get(
            "DATABASE_URL",
            "postgresql://q_bank_user:swBBhjt1SB7iEG0GlIt0OGw4qYzKGfeO@dpg-d3i0nsjipnbc73cr2ol0-a.oregon-postgres.render.com/q_bank"
        ),
        conn_max_age=600,
        ssl_require=True
    )
}

# ----------------------------
# LOCALIZATION
# ----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------
# STATIC FILES
# ----------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ----------------------------
# DEFAULT AUTO FIELD
# ----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
