from rest_framework import serializers


class UpdateMenuValidator(serializers.Serializer):
    menu_id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    image = serializers.CharField(required=False)
    is_activate = serializers.IntegerField(required=False, default=0)
    is_deactivate = serializers.IntegerField(required=False, default=0)
