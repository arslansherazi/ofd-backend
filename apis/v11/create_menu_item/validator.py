from rest_framework import serializers


class IngredientValidator(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    unit = serializers.CharField(max_length=50)
    quantity = serializers.FloatField()


class CreateMenuItemValidator(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.IntegerField()
    unit = serializers.CharField(max_length=50)
    quantity = serializers.FloatField()
    image = serializers.ImageField()
    ingredients = IngredientValidator(many=True)
    menu_id = serializers.IntegerField()
