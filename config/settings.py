import os
import dj_database_url
from pathlib import Path

# Долбоордун негизги папкасы
BASE_DIR = Path(__file__).resolve().parent.parent

# --- КООПСУЗДУК ---
# Render'де DEBUG коюлбаса, автоматтык түрдө False болот.
# Локалдык режим үчүн: DEBUG=True environment variable коюңуз.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'django-insecure-local-only'
    else:
        raise ValueError('SECRET_KEY environment variable is not set')

ALLOWED_HOSTS = [
    'lux.kg',
    'www.lux.kg',
    'ssmod-strawberry-1.onrender.com',
]

# Render'дин автоматтык берген хосту
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

if DEBUG:
    ALLOWED_HOSTS += ['localhost', '127.0.0.1']

# --- ТИРКЕМЕЛЕР ---
INSTALLED_APPS = [
    'cloudinary_storage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'cloudinary',
    'shop',
    'accounts',
]

SITE_ID = 1

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
        'DIRS': [BASE_DIR / 'templates', BASE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- МААЛЫМАТ БАЗАСЫ ---
# Серверде PostgreSQL (DATABASE_URL), локалдык режимде SQLite
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# --- ТИЛ ЖАНА УБАКЫТ ---
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True

# --- СТАТИКАЛЫК ЖАНА МЕДИА ФАЙЛДАР ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Django 4.2+ үчүн (STATICFILES_STORAGE жана DEFAULT_FILE_STORAGE ордуна)
STORAGES = {
    'default': {
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
        'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# django-cloudinary-storage collectstatic учурунда чакырган эски атрибут менен шайкештик үчүн
STATICFILES_STORAGE = STORAGES['staticfiles']['BACKEND']

# CSS ичинде табылбаган шилтемелерден улам collectstatic токтоп калбашы үчүн
WHITENOISE_MANIFEST_STRICT = False

WHITENOISE_MIME_TYPES = {
    '.mp4': 'video/mp4',
    '.mov': 'video/quicktime',
    '.webm': 'video/webm',
}

# --- CLOUDINARY ---
# Баары Render → Environment бөлүмүнөн берилет
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
    'SECURE': True,
}

# --- TELEGRAM BOTS ---
# Токендер кодго жазылбайт, Environment Variables аркылуу гана берилет
ADMIN_BOT_TOKEN = os.environ.get('ADMIN_BOT_TOKEN', '')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID', '')
DELIVERY_BOT_TOKEN = os.environ.get('DELIVERY_BOT_TOKEN', '')
DELIVERY_CHAT_ID = os.environ.get('DELIVERY_CHAT_ID', '')
SUPPORT_BOT_TOKEN = os.environ.get('SUPPORT_BOT_TOKEN', '')
SUPPORT_CHAT_ID = os.environ.get('SUPPORT_CHAT_ID', '')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'home'

# --- CSRF ЖАНА HTTPS КООПСУЗДУГУ ---
CSRF_TRUSTED_ORIGINS = [
    'https://lux.kg',
    'https://www.lux.kg',
    'https://ssmod-strawberry-1.onrender.com',
]
if RENDER_EXTERNAL_HOSTNAME:
    render_origin = f'https://{RENDER_EXTERNAL_HOSTNAME}'
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)

# Render прокси артында иштейт
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # HSTS: алгач аз убакытка, HTTPS туура иштегенин текшергенден кийин жогорулатыңыз
    SECURE_HSTS_SECONDS = 3600  # кийин 31536000 (1 жыл)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    
