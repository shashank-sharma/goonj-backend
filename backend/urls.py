from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

from .views import Home, socket_connection

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^socket/?', socket_connection, name='socket-connection'),
    url(r'^api/accounts/', include('accounts.api.urls', namespace='api-accounts')),
    url(r'^api/gov/', include('government_data.urls')),
    url(r'^docs/', include_docs_urls(title='Goonj API', permission_classes=[], public=True))
]
