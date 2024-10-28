from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'your-secret-key'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # DRF
    'drf_yasg',
    'rest_framework',
    # API 문서화 도구
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# drf-spectacular 설정
SPECTACULAR_SETTINGS = {
    'TITLE': 'My API Project',
    'DESCRIPTION': 'API documentation for my Django project.',
    'VERSION': '1.0.0',
}