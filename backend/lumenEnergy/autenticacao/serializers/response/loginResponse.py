from rest_framework import serializers

class LoginResponse(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    usuario = serializers.DictField()
