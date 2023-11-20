from django.urls import path
from .views import MyAPIView

urlpatterns = [
    path('api/', MyAPIView.as_view(), name='myapi'),
]
