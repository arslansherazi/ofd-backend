from dotenv import load_dotenv
from Crypto.Cipher import AES

load_dotenv()

basic_auth_credentials = {
    'username': os.environ('BASIC_AUTH_USERNAME'),
    'password': os.environ('BASIC_AUTH_PASSWORD')
}
keys = {
    'password_hash_key': os.environ('PASSWORD_HASH_KEY')
}
ENCRYPTION_KEY = os.environ('ENCRYPTION_KEY')
ENCRYPTION_SALT = os.environ('ENCRYPTION_SALT')
ENCRYPTION_MODE = AES.MODE_CBC
ENCRYPTION_DISABLE_KEY = os.environ('ENCRYPTION_DISABLE_KEY')
SECRET_KEY = os.environ('SECRET_KEY')
AWS_SECRET_ACCESS_KEY = os.environ('AWS_SECRET_ACCESS_KEY')
AWS_ACCESS_KEY_ID = os.environ('AWS_ACCESS_KEY_ID')
