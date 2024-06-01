from django.db import models
from django.contrib.auth.models import User


class HydroponicSystem(models.Model):
    """Hydroponic System Model"""
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hydroponic_system')
    location = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Measurement(models.Model):
    """Measurement Model"""
    hydroponic_system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE, related_name='measurements')
    ph = models.DecimalField(max_digits=4, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    tds = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hydroponic_system.title} - {self.timestamp}"
