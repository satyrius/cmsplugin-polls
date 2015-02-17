from django.conf.urls import *  # NOQA

urlpatterns = patterns('',  # NOQA
    url(r'^', include('cms.urls')),
    url(r'^polls/', include('cmsplugin_polls.urls', namespace='polls')),
)
