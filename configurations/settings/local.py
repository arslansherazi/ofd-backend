from configurations.settings.common import *

DEBUG = True
ALLOWED_HOSTS = ['192.168.10.18']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ofd_db',
        'USER': 'root',
        'PASSWORD': 'rootroot',
    }
}
API_BASE_URL = 'http://192.168.10.18:8000/ofd_apis{}'
BASE_URL = 'http://192.168.10.18:8000'
AUTH_USER_MODEL = 'apis.User'
