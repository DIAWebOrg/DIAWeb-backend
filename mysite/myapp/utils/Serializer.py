from rest_framework import serializers

class Serializer(serializers.Serializer):
    data = serializers.ListField(
        child=serializers.ListField(
            child=serializers.FloatField()
        )
    )
