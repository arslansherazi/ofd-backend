from rest_framework import serializers


class FeedbackValidator(serializers.Serializer):
    order_id = serializers.IntegerField()
    feedbacks = serializers.DictField()
