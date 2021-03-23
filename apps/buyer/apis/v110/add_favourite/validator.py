from rest_framework import serializers


class AddFavouriteValidator(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
