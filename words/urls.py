from django.conf.urls import patterns, url
from words import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'get$', views.get, name='get'),
    url(r'getTrend/(?P<keyword>.+)$', views.getTrend, name='getTrend'),
    url(r'trend/(?P<keyword>.+)$', views.trend, name='trend'),
    url(r'getNews/(?P<keyword>.+?)/(?P<pub_date>.+?)/$', views.getNews, name='getNews'),
)