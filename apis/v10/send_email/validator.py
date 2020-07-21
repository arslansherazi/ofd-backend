from rest_framework import serializers


class SendEmailValidator(serializers.Serializer):
    user_type = serializers.IntegerField()
    email = serializers.CharField()
    new_email = serializers.CharField(required=False)
    is_email_verification_code = serializers.BooleanField(required=False, default=False)
    is_forgot_password_code = serializers.BooleanField(required=False, default=False)
    is_change_email_code = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        if attrs['is_change_email_code']:
            if not attrs['new_email']:
                raise serializers.ValidationError('new_email is required')
        return attrs
