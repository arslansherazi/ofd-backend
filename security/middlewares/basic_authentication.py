import base64
import json
from urllib import parse

from django.http import HttpResponse

from common.common_helpers import CommonHelpers
from common.constants import (
    BASIC_AUTH_ENDPOINTS, INVALID_AUTHENTICATION_CREDENTIALS_MESSAGE, UNAUTHORIZED_ACCESS_MESSAGE,
    NOT_FOUND_RESPONSE_MESSAGE, WEB_ROUTING_PREFIX
)
from security.security_credentials import basic_auth_credentials


class BasicAuthenticationMiddleware(object):
    get_response = ''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # before request
        if request.path.split('/')[1] == WEB_ROUTING_PREFIX:
            decrypted_path = CommonHelpers.decrypt_data(request.path.split('/')[2])
            if request.method == 'GET':
                request.path = request.path_info = '/{request_path}'.format(request_path=decrypted_path.split('?')[0])
                request.GET = dict(parse.parse_qsl(parse.urlsplit('?{params}'.format(
                        params=decrypted_path.split('?')[1]
                )).query))
            elif request.method == 'POST':
                request.path = request.path_info = '/{request_path}'.format(request_path=decrypted_path)
        if request.path.split('/')[-1] in BASIC_AUTH_ENDPOINTS:
            basic_auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if basic_auth_header:
                basic_auth_header_token, encoded_basic_auth_header_credentials = basic_auth_header.split(' ')
                basic_auth_username = basic_auth_credentials.get('username', '')
                basic_auth_password = basic_auth_credentials.get('password', '')
                decoded_basic_auth_credentials = '{username}:{password}'.format(
                    username=basic_auth_username,
                    password=basic_auth_password
                )
                encoded_basic_auth_credentials = base64.b64encode(
                    bytes(decoded_basic_auth_credentials, 'utf-8')
                ).decode()
                if encoded_basic_auth_header_credentials != encoded_basic_auth_credentials:
                    auth_response = {
                        'message': INVALID_AUTHENTICATION_CREDENTIALS_MESSAGE,
                        'status_code': 401,
                        'success': False
                    }
                    return HttpResponse(json.dumps(auth_response), content_type='application/json', status=401)
            else:
                auth_response = {
                    'message': UNAUTHORIZED_ACCESS_MESSAGE,
                    'status_code': 401,
                    'success': False
                }
                return HttpResponse(json.dumps(auth_response), content_type='application/json', status=401)

        # calling api
        response = self.get_response(request)

        # after request
        if response.status_code == 404:
            not_found_response = {
                'message': NOT_FOUND_RESPONSE_MESSAGE,
                'status_code': 404,
                'success': False
            }
            response.content = str.encode(json.dumps(not_found_response))
            response.status_code = 404
        return response
