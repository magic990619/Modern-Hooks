from django.conf.urls import url
from vw_user.views import *


urlpatterns = [
    url(r'^$', index, name="members"),
    url(r'^edit/$', edit_member, name="edit_member"),
    url(r'^delete/$', del_member, name="del_member"),
]