from rest_framework import serializers
from .models import Test


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'a', 'b']
    
    '''
    a = serializers.IntegerField()
    b = serializers.IntegerField()
    product = serializers.IntegerField()

    def create(self, validated_data):
        return Test.objects.create(validated_data)
    '''