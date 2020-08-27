from rest_framework import serializers


class ValidateEmailValidator(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    user_type = serializers.IntegerField()
