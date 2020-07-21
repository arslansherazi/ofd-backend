import json
from urllib import parse

from common.common_helpers import CommonHelpers
from common.constants import (NO_AUTH_ENDPOINTS, NO_ENCRYPTION_ENDPOINTS,
                              SUCCESS_STATUS_CODES)
from security.security_credentials import ENCRYPTION_DISABLE_KEY


class SecurityMiddleware(object):
    get_response = ''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # before request
        params = None
        if request.method == 'POST':
            if request.POST:
                params = request.POST
            elif request.body:
                params = json.loads(request.body)
            else:
                params = {}
            encrypted_params = params.get('__prms')
            if encrypted_params:
                decrypted_params = CommonHelpers.decrypt_data(encrypted_params)
                request.POST = json.loads(decrypted_params)
                params = json.loads(decrypted_params)
        elif request.method == 'GET':
            encrypted_params = request.GET.get('__prms')
            if encrypted_params:
                decrypted_params = CommonHelpers.decrypt_data(encrypted_params)
                request.GET = dict(parse.parse_qsl(parse.urlsplit('?{decrypted_params}'.format(
                    decrypted_params=decrypted_params
                )).query))
            params = request.GET

        # calling api
        response = self.get_response(request)

        # after request
        api_endpoint = request.path.split('/')[-1]
        if (
                api_endpoint not in NO_AUTH_ENDPOINTS and
                api_endpoint not in NO_ENCRYPTION_ENDPOINTS and
                not params.get('is_forgot_password', False)
        ):
            if response.status_code in SUCCESS_STATUS_CODES:
                encryption_disable_key = params.get('encryption_disable_key', '')
                if encryption_disable_key != ENCRYPTION_DISABLE_KEY:
                    response.content = CommonHelpers.encrypt_data(str(response))
        return response
