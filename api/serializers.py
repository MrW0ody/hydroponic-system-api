from core.models import HydroponicSystem
from core.models import Measurement
from rest_framework import serializers


class HydroponicSystemSerializer(serializers.ModelSerializer):
    """Serializer for the Hydroponic System model"""

    class Meta:
        model = HydroponicSystem
        fields = '__all__'
        read_only_fields = ['id', 'user']


class MeasurementSerializer(serializers.ModelSerializer):
    """Serializer for the Measurement model"""

    class Meta:
        model = Measurement
        fields = '__all__'
        read_only_fields = ['id']
