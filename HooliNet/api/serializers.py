from rest_framework import serializers
from .models import Test


class TestSerializer(serializers.Serializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()
    product = serializers.IntegerField()

    def create(self, validated_data):
        return Test.objects.create(validated_data)