from rest_framework import serializers


class LoginValidator(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    user_type = serializers.IntegerField()
