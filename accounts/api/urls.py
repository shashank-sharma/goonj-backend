from django.conf.urls import url


from .views import UserAPIView, UserProfileAPIView, DonatorProfileAPIView, DonatorAPIView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'user/$', UserAPIView.as_view(), name='user-list'),
    url(r'^login/', obtain_jwt_token, name='login'),
    url(r'profile/(?P<pk>\d+)$', UserProfileAPIView.as_view(), name='profile'),

    url(r'^donator/(?P<pk>\d+)', DonatorProfileAPIView.as_view(), name='donator-profile'),
    url(r'^donator/?$', DonatorAPIView.as_view(), name='donator')
]