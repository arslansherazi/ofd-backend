from rest_framework import serializers


class ChangePasswordValidator(serializers.Serializer):
    is_forgot_password = serializers.BooleanField(required=False, default=False)
    old_password = serializers.CharField(required=False, max_length=100)
    new_password = serializers.CharField(required=True, max_length=100)
    change_password_token = serializers.CharField(required=False, max_length=255)
    user_id = serializers.CharField(required=False, max_length=255)

    def validate(self, attrs):
        if attrs.get('is_forgot_password'):
            if not attrs.get('change_password_token'):
                raise serializers.ValidationError('change_password_token is required')
            if not attrs.get('user_id'):
                raise serializers.ValidationError('user_id is required')
        else:
            if not attrs.get('old_password'):
                raise serializers.ValidationError('old_password is required')
        return attrs
