from django.test import TestCase
from django.contrib.auth.models import User
from ..models import HydroponicSystem
from ..models import Measurement


def create_user(username='testuser', password='testpass123'):
    """Create and return a new user"""
    return User.objects.create_user(username, password)


class TestHydroponicSystemModel(TestCase):
    """Tests the HydroponicSystem model"""

    def test_create_hydroponic_system(self):
        """Test creating a new HydroponicSystem object"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        hydroponic_system = HydroponicSystem.objects.create(
            title='System 1',
            user=user,
            location='London'
        )
        self.assertEqual(hydroponic_system.title, 'System 1')


class TestMeasurementModel(TestCase):
    """Tests the Measurement model"""

    def test_create_measurement(self):
        """Test creating a new Measurement object"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        hydroponic_system = HydroponicSystem.objects.create(
            title='System 1',
            user=user,
            location='London'
        )
        measurement = Measurement.objects.create(
            hydroponic_system=hydroponic_system,
            ph=20,
            temperature=25,
            tds=100,
        )
        self.assertEqual(measurement.hydroponic_system.title, 'System 1')


class TestUserModel(TestCase):
    """Tests the User model"""

    def test_create_user_with_username_successful(self):
        """Test creating a user with an email is successful."""
        username = 'testuser'
        password = 'testpass123'
        user = User.objects.create_user(
            username=username,
            password=password,
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_new_user_without_username_raises_error(self):
        """Test creating user with no email raises error."""
        with self.assertRaises(ValueError):
            user = User.objects.create_user('', 'sample1234')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(username='admin', password='test12345')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
