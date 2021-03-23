from rest_framework import serializers


class UpdateMenuValidator(serializers.Serializer):
    menu_id = serializers.IntegerField()
    name = serializers.CharField(required=False, max_length=100)
    image = serializers.ImageField(required=False)
    is_activate = serializers.BooleanField(required=False, default=False)
    is_deactivate = serializers.BooleanField(required=False, default=False)
