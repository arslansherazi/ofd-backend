from rest_framework import serializers


class MenuItemDetailsValidator(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
