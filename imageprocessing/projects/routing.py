from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/project/<int:project_id>/', consumers.ProjectConsumer.as_asgi()),
]
