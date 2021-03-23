from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings

from apps.user.models import User
from common.constants import (BASIC_AUTH_ENDPOINTS,
                              CHANGE_PASSWORD_API_ENDPOINT, NO_AUTH_ENDPOINTS)
from common.custom_exception_handler import CustomAPIException


class JWTTokenAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            exception_data = {
                'message': 'Token contained no recognizable user identification',
                'status_code': 401,
                'success': False
            }
            raise CustomAPIException(exception_data, status_code=401)

        try:
            user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except User.DoesNotExist:
            exception_data = {
                'message': 'User does not exist',
                'status_code': 401,
                'success': False
            }
            raise CustomAPIException(exception_data, status_code=401)
        if not user.is_active:
            exception_data = {
                'message': 'User is inactive',
                'status_code': 401,
                'success': False
            }
            raise CustomAPIException(exception_data, status_code=401)

        return user


class JWTTokenPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.end_point == CHANGE_PASSWORD_API_ENDPOINT:
            if request.POST.get('is_forgot_password', False):
                return True
        elif view.end_point in BASIC_AUTH_ENDPOINTS or view.end_point in NO_AUTH_ENDPOINTS:
            return True
        return bool(request.user and request.user.is_authenticated)
