from rest_framework import serializers


class data_Vin(serializers.Serializer):
    vin = serializers.CharField()
    EcuName = serializers.CharField()


class dataOnlyVin(serializers.Serializer):
    vin = serializers.CharField()

