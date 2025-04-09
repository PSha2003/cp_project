from django.urls import path
from .views import slack_event_hook
from .filescanview import FileScanView

urlpatterns = [
    path('slack/events/', slack_event_hook),
    path('scan/file/', FileScanView.as_view(), name='scan-file'),
]
