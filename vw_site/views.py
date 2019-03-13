# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from vw_candidate.models import Question, Candidate
from vw_jobs.models import Jobs, Questions as JobQuestions
from vw_site.models import InterviewToken


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, "vw_site/index.html")


def ssl_auth(request):
    return render(request, 'ssl_auth.html')


def interview(request, token):
    it = InterviewToken.objects.filter(token=token).first()
    if not it:
        return HttpResponseRedirect(reverse_lazy('completed_interview'))
    if it.candidate.status == 'Completed':
        return HttpResponseRedirect(reverse_lazy('completed_interview'))

    questions = Question.objects.filter(candidate=it.candidate).order_by('order')
    position = it.candidate.position
    candidate_inviter = it.candidate.user
    subclient_logo = None
    logo_position_choise = 2
    if candidate_inviter.client_group:
        if candidate_inviter.client_group.logo:
            subclient_logo = candidate_inviter.client_group.logo.url
            logo_position_choise = candidate_inviter.client_group.logo_position
    return render(request, 'vw_site/interview.html', {
        'questions': questions,
        'question_count': questions.count(),
        'position': position,
        'token': token,
        'logo_position_choise': logo_position_choise,
        'subclient_logo': subclient_logo,
    })


def universal_interview(request, user_id, position):
    if not Jobs.objects.filter(user_id=user_id, position=position).exists():
        return render(request, 'vw_site/expire.html')
    job = Jobs.objects.get(user_id=user_id)

    questions = JobQuestions.objects.filter(job_id=job.id).order_by('order')
    position = job.position
    candidate_inviter = job.user
    subclient_logo = None
    logo_position_choise = 2
    if candidate_inviter.client_group:
        if candidate_inviter.client_group.logo:
            subclient_logo = candidate_inviter.client_group.logo.url
            logo_position_choise = candidate_inviter.client_group.logo_position
    return render(request, 'vw_site/universal_interview.html', {
        'questions': questions,
        'job_id': job.id,
        'question_count': questions.count(),
        'position': position,
        'logo_position_choise': logo_position_choise,
        'subclient_logo': subclient_logo,
    })
