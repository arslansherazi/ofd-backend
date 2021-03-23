from rest_framework import serializers


class MakeTinyUrlValidator(serializers.Serializer):
    url = serializers.CharField(max_length=1000)
