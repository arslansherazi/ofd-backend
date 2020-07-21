from rest_framework import serializers


class VerifyLocationValidator(serializers.Serializer):
    location_id = serializers.IntegerField()
    address = serializers.CharField()
