from django.conf.urls import url


from .views import UserAPIView, UserProfileUpdateView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'user/$', UserAPIView.as_view(), name='user-list'),
    url(r'^login/', obtain_jwt_token, name='login'),
    url(r'profile/(?P<pk>\d+)$', UserProfileUpdateView.as_view(), name='profile')
]