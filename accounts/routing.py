from django.conf.urls import url
from accounts import consumers

websocket_urlpatterns = [
    url(r'^ws/count/(?P<token>[a-zA-Z0-9_.\-]+)/$', consumers.UserCountConsumer),
]