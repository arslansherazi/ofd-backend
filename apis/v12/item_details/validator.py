from rest_framework import serializers


class MenuItemDetailsValidator(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    menu_id = serializers.IntegerField()
