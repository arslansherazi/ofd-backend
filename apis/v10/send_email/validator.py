from rest_framework import serializers


class SendEmailValidator(serializers.Serializer):
    user_type = serializers.IntegerField()
    email = serializers.CharField(max_length=255)
    new_email = serializers.CharField(required=False, max_length=255)
    is_email_verification_code = serializers.BooleanField(required=False, default=False)
    is_forgot_password_code = serializers.BooleanField(required=False, default=False)
    is_change_email_code = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        if attrs.get('is_change_email_code'):
            if not attrs.get('new_email'):
                raise serializers.ValidationError('new_email is required')
        return attrs
