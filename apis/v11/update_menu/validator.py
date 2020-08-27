from rest_framework import serializers


class UpdateMenuValidator(serializers.Serializer):
    menu_id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    image = serializers.CharField(required=False)
    is_activate = serializers.BooleanField(required=False, default=False)
    is_deactivate = serializers.BooleanField(required=False, default=False)
