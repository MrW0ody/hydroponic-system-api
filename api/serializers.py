from core.models import HydroponicSystem
from rest_framework import serializers
from core.models import Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    """Serializer for the Measurement model"""

    class Meta:
        model = Measurement
        fields = '__all__'
        read_only_fields = ['id']


class HydroponicSystemSerializer(serializers.ModelSerializer):
    """Serializer for the Hydroponic System model"""

    class Meta:
        model = HydroponicSystem
        fields = '__all__'
        read_only_fields = ['id', 'user']
