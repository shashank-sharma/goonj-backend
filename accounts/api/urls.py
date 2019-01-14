from django.conf.urls import url


from .views import (UserAPIView,
                    UserProfileAPIView,
                    DonatorProfileAPIView,
                    DonatorAPIView,
                    WorkerAPIView,
                    WorkerProfileAPIView,
                    GoonjCenterAPIView,
                    GoonjCenterProfileAPIView,
                    VolunteerAPIView,
                    VolunteerProfileAPIView)
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'user/$', UserAPIView.as_view(), name='user-list'),
    url(r'^login/', obtain_jwt_token, name='login'),
    url(r'profile/(?P<pk>\d+)$', UserProfileAPIView.as_view(), name='profile'),
    url(r'^donator/(?P<pk>\d+)', DonatorProfileAPIView.as_view(), name='donator-profile'),
    url(r'^donator/?$', DonatorAPIView.as_view(), name='donator'),
    url(r'^worker/(?P<pk>\d+)', WorkerProfileAPIView.as_view(), name='worker-profile'),
    url(r'^worker/?', WorkerAPIView.as_view(), name='worker'),
    url(r'^goonj-center/(?P<pk>\d+)', GoonjCenterProfileAPIView.as_view(), name='goonj-center-profile'),
    url(r'^goonj-center/?', GoonjCenterAPIView.as_view(), name='goonj-center'),
    url(r'^volunteer/(?P<pk>\d+)', VolunteerProfileAPIView.as_view(), name='volunteer-profile'),
    url(r'^volunteer/?', VolunteerAPIView.as_view(), name='volunteer')
]
