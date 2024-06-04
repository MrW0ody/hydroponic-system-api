"""
Url mappings for the user API
"""
from django.urls import path
from .views import CreateUserView
from .views import CreateTokenView
from .views import ManageUserView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
]
