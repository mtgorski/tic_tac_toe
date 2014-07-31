# Fake url configuration required for testing

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ttt_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('urls', namespace='3T')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^3T/', include('urls', namespace='3T'))
)