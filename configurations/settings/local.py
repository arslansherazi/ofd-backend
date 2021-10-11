from configurations.settings.common import *

DEBUG = True
ALLOWED_HOSTS = ['192.168.43.133', '0.0.0.0', '192.168.0.104', '127.0.0.1', '192.168.0.103']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ofd_db',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'rootroot'
    }
}
API_BASE_URL = 'http://0.0.0.0:8000/ofd_apis{}'
BASE_URL = 'http://0.0.0.0:8000'
CORS_ALLOWED_ORIGINS = [
    'https://localhost:3000'
]
CORS_ALLOW_ALL_ORIGINS = True
