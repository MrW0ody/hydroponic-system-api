"""
Tests for measurement API
"""

from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from core.models import HydroponicSystem
from core.models import Measurement
from ..serializers import MeasurementSerializer
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

MEASUREMENTS_URL = reverse('api:measurement-list')


def detail_url(measurement_id):
    return reverse('api:measurement-detail', args=[measurement_id])


def create_user(username, password):
    """Create and return a new user"""
    return User.objects.create_user(username, password)


class PublicMeasurementApiTests(TestCase):
    """Test unauthenticated measurement system API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to access the API"""
        response = self.client.get(MEASUREMENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMeasurementApiTests(TestCase):
    """Test authenticated measurement system API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_measurement_list(self):
        """Test retrieving measurement list"""
        hydroponic_system = HydroponicSystem.objects.create(title='System 1', user=self.user, location='Barcelona')
        Measurement.objects.create(hydroponic_system=hydroponic_system, ph=Decimal('20'), temperature=Decimal('30'),
                                   tds=Decimal('20'))
        Measurement.objects.create(hydroponic_system=hydroponic_system, ph=Decimal('30'), temperature=Decimal('35'),
                                   tds=Decimal('20'))

        response = self.client.get(MEASUREMENTS_URL)

        measurements = Measurement.objects.all().order_by('-id')
        serializer = MeasurementSerializer(measurements, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_measurement_detail(self):
        """Test retrieving measurement detail"""
        hydroponic_system = HydroponicSystem.objects.create(title='System 1', user=self.user, location='Barcelona')
        measurement = Measurement.objects.create(hydroponic_system=hydroponic_system, ph=Decimal('20'),
                                                 temperature=Decimal('30'),
                                                 tds=Decimal('20'))
        url = detail_url(measurement.id)
        response = self.client.get(url)
        serializer = MeasurementSerializer(measurement)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_partial_update_measurement_system(self):
        """Test partial update a measurement system"""
        hydroponic_system = HydroponicSystem.objects.create(title='System 1', user=self.user, location='London')
        measurement = Measurement.objects.create(hydroponic_system=hydroponic_system, ph=Decimal('20'),
                                                 temperature=Decimal('30'),
                                                 tds=Decimal('20'))
        payload = {'ph': Decimal('30')}
        url = detail_url(measurement.id)

        response = self.client.patch(url, payload)
        measurement.refresh_from_db()
        self.assertEqual(measurement.ph, payload['ph'])
        self.assertEqual(measurement.temperature, Decimal(response.data['temperature']))

    def test_full_update_hydroponic_system(self):
        """Test full update a measurement"""
        hydroponic_system = HydroponicSystem.objects.create(title='System 1', user=self.user, location='London')
        measurement = Measurement.objects.create(hydroponic_system=hydroponic_system, ph=Decimal('20'),
                                                 temperature=Decimal('30'),
                                                 tds=Decimal('20'))
        payload = {'ph': Decimal('30'), 'temperature': Decimal('35'), 'tds': Decimal('25')}
        url = detail_url(measurement.id)

        self.client.patch(url, payload)
        measurement.refresh_from_db()
        self.assertEqual(measurement.ph, Decimal(payload['ph']))
        self.assertEqual(measurement.temperature, Decimal(payload['temperature']))
        self.assertEqual(measurement.tds, Decimal(payload['tds']))

    def test_delete_measurement(self):
        """Test deleting a measurement"""
        hydroponic_system = HydroponicSystem.objects.create(title='System 1', user=self.user, location='London')
        measurement = Measurement.objects.create(hydroponic_system=hydroponic_system, ph=Decimal('20'),
                                                 temperature=Decimal('30'),
                                                 tds=Decimal('20'))
        url = detail_url(measurement.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Measurement.objects.filter(pk=measurement.id).exists())

    def create_measurements(self):
        now = datetime.now()
        hydroponic_system = HydroponicSystem.objects.create(title='System 1', user=self.user, location='London')
        Measurement.objects.create(hydroponic_system=hydroponic_system, ph=Decimal('20'),
                                   temperature=Decimal('30'), tds=Decimal('20'), timestamp=now - timedelta(days=2))
        Measurement.objects.create(hydroponic_system=hydroponic_system, ph=Decimal('25'),
                                   temperature=Decimal('35'), tds=Decimal('25'), timestamp=now - timedelta(days=1))
        Measurement.objects.create(hydroponic_system=hydroponic_system, ph=Decimal('30'),
                                   temperature=Decimal('40'), tds=Decimal('30'), timestamp=now)

    def test_filter_measurement_by_ph_range(self):
        """Test filtering measurements by pH range"""
        self.create_measurements()
        response = self.client.get(MEASUREMENTS_URL, {'ph_min': 25, 'ph_max': 30})

        measurements = Measurement.objects.filter(ph__gte=Decimal('25'), ph__lte=Decimal('30')).order_by('-id')
        serializer = MeasurementSerializer(measurements, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_measurement_by_temperature_range(self):
        """Test filtering measurements by temperature range"""
        self.create_measurements()
        response = self.client.get(MEASUREMENTS_URL, {'temperature_min': 35, 'temperature_max': 40})

        measurements = Measurement.objects.filter(temperature__gte=Decimal('35'),
                                                  temperature__lte=Decimal('40')).order_by('-id')
        serializer = MeasurementSerializer(measurements, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_measurement_by_tds_range(self):
        """Test filtering measurements by TDS range"""
        self.create_measurements()
        response = self.client.get(MEASUREMENTS_URL, {'tds_min': Decimal('25'), 'tds_max': Decimal('30')})

        measurements = Measurement.objects.filter(tds__gte=Decimal('25'), tds__lte=Decimal('30')).order_by('-id')
        serializer = MeasurementSerializer(measurements, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
