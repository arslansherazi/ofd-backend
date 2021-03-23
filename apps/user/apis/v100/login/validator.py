from rest_framework import serializers


class LoginValidator(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    user_type = serializers.IntegerField()
