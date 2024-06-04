"""
Filters for Measurement View and HydroponicSystem View
"""

from django_filters import rest_framework as filters
from core.models import Measurement
from core.models import HydroponicSystem


class MeasurementFilter(filters.FilterSet):
    start_date = filters.DateFromToRangeFilter(field_name='timestamp', lookup_expr='gte')
    end_date = filters.DateFromToRangeFilter(field_name='timestamp', lookup_expr='lte')
    ph_min = filters.NumberFilter(field_name='ph', lookup_expr='gte')
    ph_max = filters.NumberFilter(field_name='ph', lookup_expr='lte')
    temperature_min = filters.NumberFilter(field_name='temperature', lookup_expr='gte')
    temperature_max = filters.NumberFilter(field_name='temperature', lookup_expr='lte')
    tds_min = filters.NumberFilter(field_name='tds', lookup_expr='gte')
    tds_max = filters.NumberFilter(field_name='tds', lookup_expr='lte')

    class Meta:
        model = Measurement
        fields = ['start_date', 'end_date', 'ph_min', 'ph_max', 'temperature_min', 'temperature_max', 'tds_min',
                  'tds_max']


class HydroponicSystemFilter(filters.FilterSet):
    location = filters.CharFilter(field_name='location', lookup_expr='icontains')
    created_min = filters.DateFromToRangeFilter(field_name='created', lookup_expr='gte')
    created_max = filters.DateFromToRangeFilter(field_name='created', lookup_expr='lte')
    updated_min = filters.DateFromToRangeFilter(field_name='updated', lookup_expr='gte')
    updated_max = filters.DateFromToRangeFilter(field_name='updated', lookup_expr='lte')

    class Meta:
        model = HydroponicSystem
        fields = ['location', 'created_min', 'created_max', 'updated_min', 'updated_max']
