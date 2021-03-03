from configurations.settings.common import *

DEBUG = True
ALLOWED_HOSTS = ['192.168.43.133', '0.0.0.0']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ofd_db',
        'USER': 'root',
        'PASSWORD': 'rootroot'
    }
}
API_BASE_URL = 'http://0.0.0.0:8000/ofd_apis{}'
BASE_URL = 'http://0.0.0.0:8000'
AUTH_USER_MODEL = 'apis.User'
CORS_ALLOWED_ORIGINS = [
    'https://localhost:3000'
]
CORS_ALLOW_ALL_ORIGINS = True
