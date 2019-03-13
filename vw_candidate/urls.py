from django.conf.urls import url
from vw_candidate.views import *


urlpatterns = [
    url(r'^$', index, name="dashboard"),
    url(r'^delete/(?P<pk>[\d]+)/$', CandidateDeleteView.as_view(), name="delete_candidate"),
    url(r'^create/$', CandidateDeleteView.as_view(), name="create_candidate"),
    url(r'^detail/(?P<candidate_id>[\d]+)/(?P<question_order>[\d]+)/$', CandidateDetailView.as_view(), name='detail'),
    url(r'^is_candidate_exist/$', is_candidate_exist, name='is_candidate_exist'),
    url(r'^save_interview/$', save_interview, name='save_interview'),
    url(r'^save_universal_interview/$', save_universal_interview, name='save_universal_interview'),
    url(r'^set_rating/(?P<question_id>[\d]+)/$', set_rating, name='set_rating'),
    url(r'^get_candidate_info/$', get_candidate_info, name='get_candidate_info'),
    url(r'^save_template/$', save_template, name='save_template'),
    url(r'^invites/edit/(?P<pk>[\d]+)/$', UpdateInviteMessageView.as_view(), name='edit_invite_message'),
    url(r'^invites/delete/(?P<pk>[\d]+)/$', InviteMessageDeleteView.as_view(), name='delete_invite_message'),
    url(r'^invites/', invites, name='invite_messages'),
    url(r'^upload_resume/(?P<pk>\d+)$', UploadCandidateResume.as_view(), name='upload_resume'),
    url(r'^completed_interview/$', CompletedInterView.as_view(), name='completed_interview'),
]
