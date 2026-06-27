import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')   # optional, for local dev

# ========== SECURITY ==========
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me')
DEBUG = False   # Must be False on PythonAnywhere
ALLOWED_HOSTS = ['<YOUR_USERNAME>.pythonanywhere.com']  # <--- CHANGE THIS

# ========== INSTALLED APPS ==========
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

# ========== MIDDLEWARE ==========
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crm_backend.urls'

# ========== TEMPLATES (points to your frontend) ==========
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend'],
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

WSGI_APPLICATION = 'crm_backend.wsgi.application'

# ========== DATABASE (MySQL) ==========
# Get these from PythonAnywhere "Databases" tab
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<YOUR_USERNAME>$<YOUR_DB_NAME>',   # e.g. 'johnsmith$techpro_db'
        'USER': '<YOUR_USERNAME>',                  # e.g. 'johnsmith'
        'PASSWORD': '<YOUR_MYSQL_PASSWORD>',
        'HOST': '<YOUR_USERNAME>.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}

# ========== AUTH ==========
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ========== INTERNATIONALISATION ==========
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ========== STATIC FILES ==========
STATIC_URL = '/static/'
STATIC_ROOT = f'/home/{os.environ.get("USER", "your_username")}/static'  # Absolute path
STATICFILES_DIRS = [BASE_DIR / 'frontend']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========== CORS & CSRF ==========
CORS_ALLOWED_ORIGINS = ['https://<YOUR_USERNAME>.pythonanywhere.com']
CSRF_TRUSTED_ORIGINS = ['https://<YOUR_USERNAME>.pythonanywhere.com']

# ========== REST FRAMEWORK ==========
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
