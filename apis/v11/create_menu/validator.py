from rest_framework import serializers


class CreateMenuValidator(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    image = serializers.ImageField(required=False)
