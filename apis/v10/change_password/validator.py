from rest_framework import serializers


class ChangePasswordValidator(serializers.Serializer):
    is_forgot_password = serializers.BooleanField(required=False, default=False)
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=True)
    __c_p_t = serializers.CharField(required=False)
    __ui = serializers.CharField(required=False)

    def validate(self, attrs):
        if not attrs['is_forgot_password']:
            if not attrs['old_password']:
                serializers.ValidationError('old_password is required')
        return attrs
