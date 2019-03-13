from django.conf.urls import url
from vw_question.views import *


urlpatterns = [
    url(r'^$', SampleQuestionListView.as_view(), name="questions"),
    url(r'^create/$', SampleQuestionCreateView.as_view(), name="create_question"),
    url(r'^positions_list/$', PositionsList.as_view(), name="positions_list"),
    url(r'^questions_position/$', QuestionForPosition.as_view(), name="questions_position"),
    url(r'^competencies_list/$', CompetenciesList.as_view(), name="competencies_list"),
    url(r'^questions_competency/$', QuestionForCompetency.as_view(), name="questions_competency"),
    url(r'^edit/(?P<pk>\d+)$', SampleQuestionUpdateView.as_view(), name="edit_question"),
    url(r'^delete/(?P<pk>\d+)$', SampleQuestionDeleteView.as_view(), name="del_question"),
]
