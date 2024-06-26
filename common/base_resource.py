import json

from django.shortcuts import render
from requests import codes
from rest_framework.decorators import APIView
from rest_framework.response import Response

from apps.buyer.models.v100.buyer import Buyer
from apps.merchant.models.v100.merchant import Merchant
from common.common_helpers import CommonHelpers
from common.constants import (BASIC_AUTH_ENDPOINTS, BUYER_USER_TYPE,
                              INTERNAL_SERVER_ERROR_MESSAGE, NO_AUTH_ENDPOINTS,
                              ROUTING_PREFIX, SUCCESS_STATUS_CODES)
from security.token_authentication import JWTTokenPermission


class BaseResource(APIView):
    end_point = ''
    version = ''
    request_validator = None
    # apm_client = Client(service_name=APM_SERVICE_NAME)
    status_code = 200
    permission_classes = [JWTTokenPermission]

    def request_flow(self):
        logger = None
        # bad_request = False
        try:
            if self.request.query_params:
                self.request_args = self.request.query_params
            else:
                self.request_args = self.request.data
            self.is_send_response = False
            self.response = {}
            self.current_user_info = {}
            self.http_response = None
            try:
                if self.request_validator:
                    self.request_args = self.request_validator.run_validation(data=self.request_args)
            except Exception as exception:
                # bad_request = True
                self.request_path = None
                self.handle_bad_request_response(exception)
                return self.send_response()
            self.request_path = '{routing_prefix}v{version}/{api_endpoint}'.format(
                routing_prefix=ROUTING_PREFIX, version=self.version,
                api_endpoint=self.end_point
            )
            self.set_current_user_info()
            # self.apm_client.begin_transaction(transaction_type=self.request_path)
            log_file_path = 'logs/apis/{end_point}'.format(end_point=self.end_point)
            log_file = '{end_point}_v{version}.log'.format(end_point=self.end_point, version=self.version)
            logger = CommonHelpers.get_logger(log_file_path, log_file)
            self.process_request()
            return self.send_response()
        except Exception as e:
            if logger:
                logger.exception(str(e))
                # logger.error(str(e))
                self.handle_exception_response()
                return self.send_response()
        # finally:
        #     if not bad_request:
        #         transaction_name = '{request_path}-{current_datetime}'.format(
        #             request_path=self.request_path, current_datetime=datetime.now()
        #         )
        #         self.apm_client.end_transaction(transaction_name, APM_TRANSACTION_RESULT)

    def process_request(self):
        pass

    def populate_request_arguments(self):
        pass

    def set_current_user_info(self):
        if (
                self.end_point not in BASIC_AUTH_ENDPOINTS and
                self.end_point not in NO_AUTH_ENDPOINTS and
                not self.request_args.get('is_forgot_password', False)
        ):
            self.current_user_info = {
                'user_id': self.request.user.id,
                'username': self.request.user.username,
                'email': self.request.user.email
            }
            if self.request.user.user_type == BUYER_USER_TYPE:
                self.current_user_info.update(buyer_id=Buyer().get_buyer_id(self.request.user.id))
            else:
                self.current_user_info.update(merchant_id=Merchant().get_merchant_id(self.request.user.id))

    def handle_bad_request_response(self, exception):
        param_name = list(exception.detail.keys())[0]
        response_message = exception.detail.get(param_name)[0]
        if param_name != 'non_field_errors':
            response_message = '{param_name}: {message}'.format(param_name=param_name, message=response_message)
        self.response = {
            'message': response_message
        }
        self.status_code = codes.BAD_REQUEST

    def send_response(self):
        if self.http_response:
            template_name = self.response.get('template_name')
            template_data = self.response.get('template_data')
            return render(self.request, template_name, template_data)
        final_response = self.response
        if self.request_path:
            final_response.update(cmd=self.request_path)
        final_response.update(status_code=self.status_code)
        if self.status_code in SUCCESS_STATUS_CODES:
            final_response.update(success=True)
        else:
            final_response.update(success=False)
        return Response(final_response, self.status_code)

    def handle_exception_response(self):
        self.response = {
            'message': INTERNAL_SERVER_ERROR_MESSAGE
        }
        self.status_code = codes.INTERNAL_SERVER_ERROR


class BaseGetResource(BaseResource):
    def get(self, request):
        self.request = request
        return self.request_flow()


class BasePostResource(BaseResource):
    def post(self, request):
        self.request = request
        return self.request_flow()


class BasePutResource(BaseResource):
    def put(self, request):
        self.request = request
        return self.request_flow()


class BaseDeleteResource(BaseResource):
    def delete(self, request):
        self.request = request
        return self.request_flow()
