from rest_framework import serializers


class VerifyEmailValidator(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.IntegerField()
    old_email = serializers.CharField(required=False, max_length=255)
    new_email = serializers.CharField(required=False, max_length=255)
    change_password_token = serializers.CharField(required=False, max_length=255)
    is_forgot_password_code = serializers.BooleanField(default=False, required=False)
    is_email_verification_code = serializers.BooleanField(default=False, required=False)
    is_change_email_code = serializers.BooleanField(default=False, required=False)

    def validate(self, attrs):
        if attrs.get('is_change_email_code'):
            if not attrs.get('old_email'):
                raise serializers.ValidationError('old_email is required')
            if not attrs.get('new_email'):
                raise serializers.ValidationError('new_email is required')
        if attrs.get('is_forgot_password_code'):
            if not attrs.get('change_password_token'):
                raise serializers.ValidationError('change_password_token is required')
        return attrs
