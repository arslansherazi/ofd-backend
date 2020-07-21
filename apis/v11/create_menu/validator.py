from rest_framework import serializers


class CreateMenuValidator(serializers.Serializer):
    name = serializers.CharField()
    image = serializers.ImageField(required=False)
