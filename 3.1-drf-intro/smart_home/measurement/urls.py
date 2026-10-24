from django.urls import path
from .views import (
    SensorCreateView,
    SensorListView,
    SensorDetailView,
    MeasurementCreateView
)

urlpatterns = [
    path('sensors/create/', SensorCreateView.as_view(), name='sensor-create'),
    path('sensors/', SensorListView.as_view(), name='sensor-list'),
    path('sensors/<int:pk>/', SensorDetailView.as_view(), name='sensor-detail'),
    path('measurements/create/', MeasurementCreateView.as_view(), name='measurement-create'),
]