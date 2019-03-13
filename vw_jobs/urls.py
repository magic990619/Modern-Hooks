from django.conf.urls import url

from .views import JobListView, JobUpdateView, JobDeleteView, JobCreateView, JobQuestionCreateView

urlpatterns = [
    url(r'^create/question/$', JobQuestionCreateView.as_view(), name="create_job_question"),
    url(r'^create/$', JobCreateView.as_view(), name="create_job"),
    url(r'^delete/(?P<pk>\d+)/$', JobDeleteView.as_view(), name="delete_job"),
    url(r'^update/(?P<pk>\d+)/$', JobUpdateView.as_view(), name="update_job"),
    url(r'^$', JobListView.as_view(), name="list_job"),
]
