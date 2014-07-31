from django.conf.urls import patterns, url
from ttt_app import views


urlpatterns = patterns('',
                       url(r'^$', views.launch, name='launch'),
                       url(r'^play$', views.play, name='play'),
                       url(r'^advance/(true|false)/([xo-]{9})$', views.advance, name='advance'))