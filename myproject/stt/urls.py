from django.urls import path
from .views import index, StartRecordingAPIView, StopRecordingAPIView

urlpatterns = [
    path('', index, name='index'),
    path('stt/start-recording/', StartRecordingAPIView.as_view(), name='start-recording'),
    path('stt/stop-recording/', StopRecordingAPIView.as_view(), name='stop-recording'),
]
