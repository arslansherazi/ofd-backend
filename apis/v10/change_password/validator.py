from rest_framework import serializers


class ChangePasswordValidator(serializers.Serializer):
    is_forgot_password = serializers.BooleanField(required=False, default=False)
    old_password = serializers.CharField(required=False, max_length=100)
    new_password = serializers.CharField(required=True, max_length=100)
    __c_p_t = serializers.CharField(required=False, max_length=255)
    __ui = serializers.CharField(required=False, max_length=255)

    def validate(self, attrs):
        if not attrs.get('is_forgot_password'):
            if not attrs.get('old_password'):
                serializers.ValidationError('old_password is required')
        return attrs
