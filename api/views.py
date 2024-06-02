from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework.response import Response
from core.models import HydroponicSystem
from core.models import Measurement
from .serializers import HydroponicSystemSerializer
from .serializers import MeasurementSerializer


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    """ViewSet for the HydroponicSystem Model"""
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MeasurementViewSet(viewsets.ModelViewSet):
    """ViewSet for the Measurement Model"""
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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
