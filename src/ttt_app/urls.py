from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
                       url(r'^$', views.launch, name='launch'),
                       url(r'^play$', views.play, name='play'))