from rest_framework import serializers


class IngredientValidator(serializers.Serializer):
    name = serializers.CharField()
    unit = serializers.CharField()
    quantity = serializers.FloatField()


class CreateMenuItemValidator(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()
    unit = serializers.CharField()
    quantity = serializers.FloatField()
    image = serializers.CharField()
    ingredients = IngredientValidator(many=True)
    menu_id = serializers.IntegerField()
