# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, ListView, DeleteView, CreateView, DetailView, TemplateView

from anytimeiv.settings import EMAIL_DOMAIN, EMAIL_API, EMAIL_SUPPORT
from vw_client_groups.models import SubClientGroup
from vw_jobs.models import Jobs, Questions as JobQuestions
from vw_question.models import SampleQuestion, Position
from vw_question.views import AjaxRequestMixin
from vw_site.models import InterviewToken
from vw_user.models import InviteTemplate
from .forms import InterviewForm, UniversalInterviewForm
from .models import Candidate, Question, Recording, Rating

invite_link_str = '%3C%3CInvite%20Link%3E%3E'


@login_required
def index(request):
    """
    TODO: rewrite this piece of shit
    """
    user = request.user
    questions = SampleQuestion.objects.filter(user=user)
    invites = InviteTemplate.objects.filter(user=user).order_by('-id')
    positions = Position.objects.filter(user=user)
    subclient_groups = SubClientGroup.objects.filter(users=user)

    protocol = 'https' if request.is_secure() else 'http'
    site_url = "{0}://{1}/interview/".format(protocol,
                                             request.META.get('HTTP_HOST', settings.SITE_URL), )
    if user.client_group:
        candidates = Candidate.objects.filter(client_group=user.client_group)
    else:
        ids_user_subclients = user.subclientgroup_set.values_list('id', flat=True)
        candidates = Candidate.objects.filter(subclient_group__id__in=ids_user_subclients)
    candidates = candidates.union(Candidate.objects.filter(user=user))
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        invite_message = request.POST.get('invite_message')
        position = request.POST.get('position')
        selected_subclient_group = request.POST.get('subclient_group')
        subclient_group = SubClientGroup.objects.filter(
            title=selected_subclient_group, users=user
        ).first()
        # check if invited candidate is already exist

        if Candidate.objects.filter(user=user, email=email).exists():
            return render(request, "vw_candidate/index.html", {
                'candidates': candidates,
                'questions': questions,
                'invites': invites,
                'invitesList': list(invites),
                'SITE_URL': site_url,
                'positions': positions
            })
        if user.client_group:
            new_candidate = Candidate.objects.create(
                user=user, email=email, position=position, status="Incomplete",
                client_group=user.client_group, first_name=first_name, invite_message=invite_message
            )
        elif subclient_group:
            new_candidate = Candidate.objects.create(
                user=user, email=email, position=position, status="Incomplete",
                subclient_group=subclient_group, client_group=subclient_group.client_group, first_name=first_name,
                invite_message=invite_message
            )
        else:
            new_candidate = Candidate.objects.create(
                user=user, email=email, position=position, status="Incomplete", first_name=first_name,
                invite_message=invite_message
            )
        # create questions
        for i in range(1, 11):
            question = request.POST.get('question%d' % i)
            if not question:
                break
            limit = request.POST.get('limit%d' % i)
            sample_question = SampleQuestion.objects.filter(content__icontains=question).first()
            if sample_question:
                competency = sample_question.competency
            else:
                competency = None
            Question.objects.create(
                candidate=new_candidate, ques=question, limit=float(limit), order=i,
                competency=competency
            )

        # generate token
        invite_link = request.POST.get('invite_link')
        invite_html = request.POST.get('invite_message')
        token = invite_link.replace(site_url, '')

        InterviewToken.objects.create(candidate=new_candidate, token=token)
        # send invite email
        send_email(EMAIL_SUPPORT, [email], "Job Interview", invite_html)

    return render(request, "vw_candidate/index.html", {
        'candidates': candidates,
        'questions': questions,
        'subclient_groups': subclient_groups,
        'invites': invites,
        'invitesList': list(invites),
        'SITE_URL': site_url,
        'positions': positions
    })


class CandidateDeleteView(AjaxRequestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'vw_candidate/index.html'
    model = Candidate
    success_url = '/candidates/'


class CandidateCreateView(AjaxRequestMixin, LoginRequiredMixin, CreateView):
    model = Candidate
    form_class = ''
    template_name = 'vw_candidate/create_form.html'


class CandidateListView(LoginRequiredMixin, ListView):
    context_object_name = 'candidates'
    model = Candidate
    template_name = "vw_candidate/index.html"

    def get_context_data(self, **kwargs):
        context = super(CandidateListView, self).get_context_data(**kwargs)
        questions = SampleQuestion.objects.filter(user=self.request.user)
        invites = InviteTemplate.objects.filter(user=self.request.user)
        positions = Position.objects.filter(user=self.request.user)

        protocol = self.request.is_secure() or 'http'
        site_url = "{0}://{1}/interview/".format(protocol, self.request.META.get('HTTP_HOST',
                                                                                 settings.SITE_URL), )
        context.update({
            'questions': questions,
            'invites': invites,
            'invitesList': list(invites),
            'SITE_URL': site_url,
            'positions': positions
        })


class CandidateDetailView(LoginRequiredMixin, DetailView):
    model = Candidate
    context_object_name = 'candidate'
    template_name = "candidates/candidate_detail_view.html"
    pk_url_kwarg = 'candidate_id'

    def get_context_data(self, **kwargs):
        """
        Add some fields for current candidate context
        :param kwargs: candidate_id, question_order
        :return: changed context in a dict
        """
        sel_candidate = Candidate.objects.get(pk=self.kwargs['candidate_id'])
        candidates = self.request.user.candidate_set.filter(status="Completed")
        question_count = sel_candidate.question_set.count()
        question = Question.objects.filter(candidate_id=self.kwargs['candidate_id'],
                                           order=self.kwargs['question_order']).first()
        context = super(CandidateDetailView, self).get_context_data(**self.kwargs)
        question_set = sel_candidate.question_set.all().order_by('order')
        try:
            candidate_rate = question.recording.rating_set.get(user=self.request.user).rate
        except (Rating.DoesNotExist, Recording.DoesNotExist):
            candidate_rate = 0
        context.update({
            'sel_candidate': sel_candidate,
            'created_at': (sel_candidate.created_at + datetime.timedelta(hours=11)).strftime("%d-%m-%Y %I:%M %p"),
            'candidates': candidates,
            'question_count': question_count,
            'question_loop': range(1, question_count + 1),
            'question_order': self.kwargs['question_order'],
            'question': question,
            'question_rate': candidate_rate,
            'question_set': question_set

        })
        return context


@csrf_exempt
def save_interview(request):
    if request.method == 'POST':
        form = InterviewForm(request.POST, request.FILES)
        if form.is_valid():
            token = form.cleaned_data['token']
            interviewToken = InterviewToken.objects.get(token=token)
            candidate = interviewToken.candidate

            recording = Recording()
            question_order = form.cleaned_data['question_order']
            recording.question = \
                Question.objects.filter(candidate=candidate, order=question_order)[0]
            recording.video = form.cleaned_data['video']
            recording.save()

            candidate.created_at = datetime.datetime.now()
            if question_order == 1:
                candidate.first_name = form.cleaned_data['first_name']
                candidate.last_name = form.cleaned_data['last_name']
                candidate.save()
            if question_order == form.cleaned_data['question_count']:
                candidate.status = 'Completed'
                candidate.save()
                interviewToken.delete()
            return HttpResponse('success')
    return HttpResponse('fail')


@csrf_exempt
def save_universal_interview(request):
    if request.method == 'POST':
        form = UniversalInterviewForm(request.POST, request.FILES)
        if form.is_valid():
            job = Jobs.objects.get(id=form.cleaned_data['job_id'])
            candidate, _ = Candidate.objects.get_or_create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                position=form.cleaned_data['position'],
                user_id=job.user_id
            )
            q = JobQuestions.objects.get(job_id=job.id, order=form.cleaned_data['question_order'])
            Question.objects.create(
                candidate=candidate,
                ques=q.question,
                limit=q.limit,
                order=q.order,
                competency=q.competency,
            )
            recording = Recording()
            question_order = form.cleaned_data['question_order']
            recording.question = Question.objects.filter(
                candidate=candidate, order=question_order
            )[0]
            recording.video = form.cleaned_data['video']
            recording.save()

            candidate.created_at = datetime.datetime.now()
            if question_order == 1:
                candidate.first_name = form.cleaned_data['first_name']
                candidate.last_name = form.cleaned_data['last_name']
                candidate.save()
            if question_order == form.cleaned_data['question_count']:
                candidate.status = 'Completed'
                candidate.save()
            return HttpResponse('success')
    return HttpResponse('fail')


@login_required
def set_rating(request, question_id):
    recording = Recording.objects.get(question_id=question_id)
    rate = request.POST.get('rating')
    data = {'user': request.user, 'recording': recording, }
    rating, _ = Rating.objects.get_or_create(**data)
    rating.rate = int(rate)
    rating.save()
    candidate = recording.question.candidate
    return HttpResponse(json.dumps({
        'avg_rate_html': render_to_string('candidates/includes/avg_rate.html', {'candidate': candidate}),
        'score_html': render_to_string('candidates/includes/score.html', {'candidate': candidate}),
    }), content_type='application/json')


@login_required
@csrf_exempt
def get_candidate_info(request):
    candidate_id = request.POST.get('candidate_id')
    candidate = Candidate.objects.get(pk=candidate_id)

    protocol = 'https' if request.is_secure() else 'http'
    site_url = "{0}://{1}/interview/{0}".format(
        protocol, request.META.get('HTTP_HOST', settings.SITE_URL),
        candidate.interviewtoken_set.last()
    )
    return HttpResponse(json.dumps({
        'email': candidate.email,
        'site_url': site_url,
        'position': candidate.position,
        'questions': [question.ques for question in candidate.question_set.all()],
        'limits': [question.limit for question in candidate.question_set.all()],
    }), content_type='application/json')


def is_candidate_exist(request):
    error_messages = {
        'position': 'Please select position for candidate',
        'email': 'Please enter email for candidate'

    }
    for error in error_messages.keys():
        if not request.POST.get(error):
            return HttpResponse(error_messages[error])
    return HttpResponse('false')


@login_required
@csrf_exempt
def save_template(request):
    template_id = request.POST.get('template_id', None)
    html = request.POST.get('html', '')
    invite_link = request.POST.get('invite_link', None)
    html = html.replace(invite_link, invite_link_str)

    if template_id:
        inviteTemplate = InviteTemplate.objects.get(pk=template_id)
        inviteTemplate.html = html
        inviteTemplate.save()
    else:
        inviteTemplate = InviteTemplate(user=request.user, html=html)
        inviteTemplate.save()
    return HttpResponse('true')


class InviteMessageDeleteView(AjaxRequestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'vw_candidate/invite_templates.html'
    model = InviteTemplate
    success_url = '/candidates/invites/'


@login_required
@csrf_exempt
def invites(request):
    request_type = request.POST.get('action')
    if request_type == 'delete':
        del_id = request.POST.get('del_id', None)
        InviteTemplate.objects.get(pk=del_id).delete()
    elif request_type == 'add':
        html = request.POST.get('content')
        is_global = request.POST.get('is_global', False)
        InviteTemplate.objects.create(user=request.user, html=html, is_global=is_global)
    return render(request, "vw_candidate/invite_templates.html", {
        'invites': InviteTemplate.objects.filter(Q(user=request.user) | Q(is_global=True)),
    })


@login_required
@csrf_exempt
def edit_invite(request):
    content = request.POST.get('content')
    message_id = request.POST.get('message_id')
    message = InviteTemplate.objects.get(pk=message_id)
    message.html = content
    message.save()
    return HttpResponse('success')


def send_email(from_email, to_emails, subject, html):
    requests.post(
        'https://api.mailgun.net/v3/%s/messages' % EMAIL_DOMAIN,
        auth=('api', EMAIL_API),
        data={
            'from': from_email,
            'to': to_emails,
            'subject': subject,
            'text': '',
            'html': html,
        }
    )


class UploadCandidateResume(LoginRequiredMixin, UpdateView):
    model = Candidate
    fields = ('resume',)
    success_url = '/'


class UpdateInviteMessageView(LoginRequiredMixin, UpdateView):
    model = InviteTemplate
    fields = '__all__'
    success_url = '/'
    template_name = 'vw_candidate/includes/edit_interview.html'

    def get_success_url(self):
        return reverse_lazy('invite_messages')


class CompletedInterView(TemplateView):
    template_name = 'candidates/completed_interview.html'
