"""
Tests for hydroponic system API
"""

from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from core.models import HydroponicSystem
from ..serializers import HydroponicSystemSerializer
from ..serializers import HydroponicSystemDetailSerializer
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

HYDROPONIC_SYSTEM_URL = reverse('api:hydroponicsystem-list')


def detail_url(hydroponicsystem_id):
    return reverse('api:hydroponicsystem-detail', args=[hydroponicsystem_id])


def create_user(username, password):
    """Create and return a new user"""
    return User.objects.create_user(username, password)


class PublicHydroponicSystemApiTests(TestCase):
    """Test unauthenticated hydroponic system API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to access the API"""
        response = self.client.get(HYDROPONIC_SYSTEM_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateHydroponicSystemApiTests(TestCase):
    """Test authenticated hydroponic system API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_hydroponic_system(self):
        """Test retrieving hydroponic system"""
        HydroponicSystem.objects.create(title='System 1', user=self.user, location='London')
        HydroponicSystem.objects.create(title='System 2', user=self.user, location='Barcelona')

        response = self.client.get(HYDROPONIC_SYSTEM_URL)

        hydroponic_system = HydroponicSystem.objects.all().order_by('-id')
        serializer = HydroponicSystemSerializer(hydroponic_system, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_hydroponic_system_detail(self):
        """Test retrieving hydroponic system detail"""
        hydroponic_system = HydroponicSystem.objects.create(title='System 1', user=self.user, location='London')
        url = detail_url(hydroponic_system.id)
        response = self.client.get(url)
        serializer = HydroponicSystemDetailSerializer(hydroponic_system)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_partial_update_hydroponic_system(self):
        """Test partial update a hydroponic system"""
        hydroponic_system = HydroponicSystem.objects.create(title='System 1', user=self.user, location='London')
        payload = {'title': 'System 2'}
        url = detail_url(hydroponic_system.id)

        response = self.client.patch(url, payload)
        hydroponic_system.refresh_from_db()
        self.assertEqual(hydroponic_system.title, payload['title'])
        self.assertEqual(hydroponic_system.location, response.data['location'])
        self.assertEqual(hydroponic_system.user, self.user)

    def test_full_update_hydroponic_system(self):
        """Test full update a hydroponic system"""
        hydroponic_system = HydroponicSystem.objects.create(title='System 1', user=self.user, location='London')
        payload = {'title': 'System 2', 'location': 'Barcelona'}
        url = detail_url(hydroponic_system.id)

        self.client.patch(url, payload)
        hydroponic_system.refresh_from_db()
        self.assertEqual(hydroponic_system.title, payload['title'])
        self.assertEqual(hydroponic_system.location, payload['location'])
        self.assertEqual(hydroponic_system.user, self.user)

    def test_update_user_error_hydroponic_system(self):
        """Test changing the hydroponic system to an invalid user"""
        new_user = create_user(username='testuser2', password='testpass123')
        hydroponic_system = HydroponicSystem.objects.create(title='System 1', user=self.user, location='London')
        payload = {'user': new_user.id}

        url = detail_url(hydroponic_system.id)
        self.client.patch(url, payload)
        hydroponic_system.refresh_from_db()

        self.assertEqual(hydroponic_system.user, self.user)

    def test_delete_hydroponic_system(self):
        """Test deleting a hydroponic system"""
        hydroponic_system = HydroponicSystem.objects.create(title='System 1', user=self.user, location='London')
        url = detail_url(hydroponic_system.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(HydroponicSystem.objects.filter(pk=hydroponic_system.id).exists())

    def test_filter_hydroponic_system_by_location(self):
        """Test filtering hydroponic systems by location"""
        HydroponicSystem.objects.create(title='System 1', user=self.user, location='London')
        HydroponicSystem.objects.create(title='System 2', user=self.user, location='Barcelona')
        HydroponicSystem.objects.create(title='System 3', user=self.user, location='New York')

        response = self.client.get(HYDROPONIC_SYSTEM_URL, {'location': 'London'})
        systems = HydroponicSystem.objects.filter(location__icontains='London')
        serializer = HydroponicSystemSerializer(systems, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_hydroponic_system_by_created_date_range(self):
        """Test filtering hydroponic systems by user by created date"""
        now = datetime.now()
        HydroponicSystem.objects.create(title='System 1', user=self.user, location='London',
                                        created=now - timedelta(days=10))
        HydroponicSystem.objects.create(title='System 2', user=self.user, location='Barcelona',
                                        created=now - timedelta(days=5))
        HydroponicSystem.objects.create(title='System 3', user=self.user, location='New York', created=now)

        start_date = now.date()

        response = self.client.get(HYDROPONIC_SYSTEM_URL, {'created': start_date})
        systems = HydroponicSystem.objects.filter(created__date__gte=start_date)
        HydroponicSystemSerializer(systems, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_hydroponic_system_by_updated_date_range(self):
        """Test filtering hydroponic systems by user by updated date"""
        now = datetime.now()
        HydroponicSystem.objects.create(title='System 1', user=self.user, location='London',
                                        updated=now - timedelta(days=10))
        HydroponicSystem.objects.create(title='System 2', user=self.user, location='Barcelona',
                                        updated=now - timedelta(days=5))
        HydroponicSystem.objects.create(title='System 3', user=self.user, location='New York', updated=now)

        start_date = (now - timedelta(days=7)).date()
        end_date = now.date()

        response = self.client.get(HYDROPONIC_SYSTEM_URL, {'updated_min': start_date, 'updated_max': end_date})
        systems = HydroponicSystem.objects.filter(updated__date__gte=start_date, updated__date__lte=end_date)
        HydroponicSystemSerializer(systems, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
