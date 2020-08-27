APM_TRANSACTION_RESULT = 'Completed'
APM_SERVICE_NAME = 'OFD'
SYSTEM_SENDER_EMAIL = 'arslan.python.dev@gmail.com'
EMAIL_VERIFICATION_SUBJECT = 'OFD - Email Verification'
CHANGE_PASSWORD_SUBJECT = 'OFD - Change Password'
PAKISTAN_TIME_ZONE = 'Asia/Karachi'
MENU_ITEM_IMAGE_DIMENSIONS = (500, 300)
PROFILE_IMAGE_DIMENSIONS = (250, 250)
MENU_IMAGE_DIMENSIONS = (400, 250)
PNG_IMAGE_EXTENSION = 'png'
SUCCESS_STATUS_CODES = [200, 201]
IMAGES_BASE_URL = 'https://onlinefooddepot.pythonanywhere.com/ofd_files'
ASSETS_BASE_URL = 'https://onlinefooddepot.pythonanywhere.com/ofd_assets/'
BASIC_AUTH_ENDPOINTS = [
    'login', 'signup', 'validate_email', 'send_email', 'api_token', 'verify_location', 'merchants', 'get_location_id'
]
NO_AUTH_ENDPOINTS = ['verify_email']
ROUTING_PREFIX = 'ofd_apis/'
INVALID_AUTHENTICATION_CREDENTIALS_MESSAGE = 'Invalid authentication credentials'
UNAUTHORIZED_ACCESS_MESSAGE = 'Unauthorized access'
INTERNAL_SERVER_ERROR_MESSAGE = 'Internal server error'
BAD_REQUEST_MESSAGE = 'Bad Request'
NOT_FOUND_RESPONSE_MESSAGE = '404 Not Found'
EMAIL_VERIFICATION_MESSAGE = 'Email is verified successfully'
EMAIL_VERIFICATION_LINK_ERROR_MESSAGE = 'Something went wrong. Please request a new link from app.'
EMAIL_ALREADY_VERIFIED_MESSAGE = 'Email already verified'
WEB_ROUTING_PREFIX = 'mQdRKp5NMj'
LINK_EXPIRED_MESSAGE = 'This link is expired. Please request a new link from app.'
NO_ENCRYPTION_ENDPOINTS = ['api_token', 'validate_email']
CHANGE_PASSWORD_API_ENDPOINT = 'change_password'
EMAIL_VERIFICATION_LINK_EXPIRATION_TIME = 24  # hours
BUYER_USER_TYPE = 1
MERCHANT_USER_TYPE = 2
MERCHANTS = 'merchants'
BUYERS = 'buyers'
AVERAGE_PREPARATION_TIME = 20
BUFFER_TIME = 10
ITEMS_LISTING_PAGE_LIMIT = 10
FUZZY_SCORE = 50
DEFAULT_ITEMS_LIMIT = 5
FUZZY_SEARCH_RECORDS_LIMIT = 9999999999
BUYER_ADDRESSES_LIMIT = 7
