from django.conf.urls import patterns, url
from ttt_app import views


urlpatterns = patterns('',
                       url(r'^$', views.launch, name='launch'),
                       url(r'^play$', views.play, name='play'),
                       # There needs to be an unambigous way to refer to the
                       # first part of the advance url, but reverse("3T:advance")
                       # won't work since advance expects arguments.
                       url(r'^advance$', views.advance_start, name='advance_start'),
                       url(r'^advance/(true|false)/([xo-]{9})$', views.advance, name='advance'))