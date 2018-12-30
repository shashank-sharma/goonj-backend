from django.conf.urls import url


from .views import UserAPIView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'user/$', UserAPIView.as_view(), name='user-list'),
    url(r'^login/', obtain_jwt_token, name='login'),
]