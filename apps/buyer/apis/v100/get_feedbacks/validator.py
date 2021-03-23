from rest_framework import serializers


class FeedbacksValidator(serializers.Serializer):
    item_id = serializers.IntegerField()
