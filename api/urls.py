from django.urls import path
from django.urls import include
from rest_framework import routers
from .views import HydroponicSystemViewSet
from .views import MeasurementViewSet

router = routers.DefaultRouter()
router.register('systems', HydroponicSystemViewSet)
router.register('measurements', MeasurementViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
