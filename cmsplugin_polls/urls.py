from django.conf.urls import patterns, url
from cmsplugin_polls import views

urlpatterns = patterns('',  # NOQA
    url(r'^vote/?$', views.vote, name='vote'),
)
