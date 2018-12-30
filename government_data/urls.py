from django.conf.urls import url
from government_data.api import views as api_views

urlpatterns = [
    url(r'weather/(?P<pk>[a-zA-Z]+)?$', api_views.WeatherView.as_view()),
    url(r'disease/(((?P<year>[0-9]+)/)?((?P<week>[0-9]+)/)?)?$', api_views.DiseaseView.as_view()),
    url(r'alert/earthquake/(?P<year>[0-9]+)?$', api_views.EarthQuakeView.as_view()),
]