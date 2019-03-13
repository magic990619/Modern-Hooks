from django.conf.urls import url
from vw_site.views import *


urlpatterns = [
    url(r'^job/(?P<user_id>[-\d]+)/(?P<position>[-\w]+)/$', universal_interview, name='universal_interview'),
    url(r'^$', index, name="index"),
    url(r'^interview/(?P<token>[-\w]+)/$', interview, name='interview'),
    url(r'^.well-known/pki-validation/fileauth.txt$', ssl_auth),
]
