from rest_framework import serializers


class ValidateEmailValidator(serializers.Serializer):
    email = serializers.CharField()
    user_type = serializers.CharField()
