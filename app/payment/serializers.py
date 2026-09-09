from rest_framework import serializers


class ZarinpalCallbackSerializer(serializers.Serializer):
    Authority = serializers.CharField(required=True)
    Status = serializers.CharField(required=True)