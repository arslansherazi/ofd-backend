from rest_framework import serializers


class GetProfileValidator(serializers.Serializer):
    user_type = serializers.IntegerField()
