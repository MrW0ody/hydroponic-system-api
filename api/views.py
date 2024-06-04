"""
View for HydroponicSystem and Measurement model
"""

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework.response import Response
from core.models import HydroponicSystem
from core.models import Measurement
from .serializers import HydroponicSystemSerializer
from .serializers import HydroponicSystemDetailSerializer
from .serializers import MeasurementSerializer
from .filters import MeasurementFilter
from .filters import HydroponicSystemFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    """ViewSet for the HydroponicSystem Model"""
    queryset = HydroponicSystem.objects.all().select_related('user')
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = HydroponicSystemFilter
    ordering_fields = ['created', 'updated']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HydroponicSystemDetailSerializer
        return HydroponicSystemSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a hydroponic system along with its latest 10 measurements"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if self.action == 'retrieve':
            measurements = Measurement.objects.filter(hydroponic_system=instance).order_by('-timestamp')[:10]
            data['measurements'] = MeasurementSerializer(measurements, many=True).data
        return Response(data)


class MeasurementViewSet(viewsets.ModelViewSet):
    """ViewSet for the Measurement Model"""
    queryset = Measurement.objects.all().select_related('hydroponic_system', 'hydroponic_system__user')
    serializer_class = MeasurementSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MeasurementFilter
    ordering_fields = ['timestamp', 'ph', 'temperature', 'tds']

    def get_queryset(self):
        return self.queryset.filter(hydroponic_system__user=self.request.user).order_by('-id')

    def create(self, request, *args, **kwargs):
        """Handle POST request"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hydroponic_system_id = serializer.validated_data['hydroponic_system'].id
        hydroponic_system = HydroponicSystem.objects.get(id=hydroponic_system_id)

        if hydroponic_system.user == self.request.user:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"detail": "You do not have permission to add measurements to this system."},
                            status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        """We block change hydroponic_system to update the measurement object"""
        instance = self.get_object()
        if 'hydroponic_system' in request.data and request.data['hydroponic_system'] != instance.hydroponic_system.id:
            return Response({"detail": "You cannot change the hydroponic system of this measurement."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)
