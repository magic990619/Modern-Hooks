# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.http import JsonResponse, StreamingHttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import SampleQuestionForm
from .models import SampleQuestion, Position, Competency


class AjaxRequestMixin(object):
    success_url = '/'

    def form_invalid(self, form):
        data = {
            'status': 'error',
            'form': render_to_string(self.template_name, {'form': form}, request=self.request)}
        return JsonResponse(data)

    def form_valid(self, form):
        data = {'status': 'ok'}
        return JsonResponse(data)


class SampleQuestionCreateView(AjaxRequestMixin, LoginRequiredMixin, CreateView):
    model = SampleQuestion
    form_class = SampleQuestionForm
    template_name = 'vw_question/create_form.html'
    success_url = '/'

    def form_valid(self, form):
        form_data = form.save(commit=False)
        form_data.user = self.request.user
        if self.request.POST.get('position'):
            role, _ = Position.objects.get_or_create(
                name=self.request.POST['position'],
                user=self.request.user
            )
            form_data.position = role
        if self.request.POST.get('competency'):
            role, _ = Competency.objects.get_or_create(
                name=self.request.POST['competency']
            )
            form_data.competency = role
        form_data.save()
        return super(SampleQuestionCreateView, self).form_valid(form)


class PositionsList(LoginRequiredMixin, View):
    http_method_names = ['get']
    queryset = Position.objects.all()

    def get_queryset(self, request):
        self.queryset = self.queryset.filter(user_id=self.request.user.id)
        if request.GET.get('position'):
            return self.queryset.filter(name__icontains=request.GET.get('position'))
        else:
            return self.queryset

    def get(self, request, *args, **kwargs):
        return StreamingHttpResponse(
            serializers.serialize('json', list(self.get_queryset(request)), fields=('name', 'id')),
            content_type='application/json'
        )


class QuestionForPosition(LoginRequiredMixin, View):
    http_method_names = ['get']
    queryset = SampleQuestion.objects.all()

    def get_queryset(self, request):
        self.queryset = self.queryset.filter(user_id=self.request.user.id)
        if request.GET.get('position'):
            return self.queryset.filter(position__name=request.GET.get('position'))
        else:
            return self.queryset.none()

    def get(self, request, *args, **kwargs):
        return StreamingHttpResponse(
            serializers.serialize('json', list(self.get_queryset(request)),
                                  fields=('content', 'id', 'limit',)),
            content_type='application/json'
        )


class CompetenciesList(LoginRequiredMixin, View):
    http_method_names = ['get']
    queryset = Competency.objects.all()

    def get_queryset(self, request):
        if request.GET.get('competency'):
            return self.queryset.filter(name__icontains=request.GET.get('competency'))
        else:
            return self.queryset

    def get(self, request, *args, **kwargs):
        return StreamingHttpResponse(
            serializers.serialize('json', list(self.get_queryset(request)), fields=('name', 'id')),
            content_type='application/json'
        )


class QuestionForCompetency(LoginRequiredMixin, View):
    http_method_names = ['get']

    def get_queryset(self, request):
        if request.GET.get('competency'):
            return SampleQuestion.objects.filter(competency__name=request.GET.get('competency'))
        else:
            return SampleQuestion.objects.none()

    def get(self, request, *args, **kwargs):
        return StreamingHttpResponse(
            serializers.serialize('json', list(self.get_queryset(request)),
                                  fields=('content', 'id')),
            content_type='application/json'
        )


class SampleQuestionDeleteView(AjaxRequestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'vw_question/form_delete.html'
    model = SampleQuestion

    def get_success_url(self):
        return reverse_lazy('questions')


class SampleQuestionListView(LoginRequiredMixin, ListView):
    model = SampleQuestion
    template_name = "vw_question/index.html"
    context_object_name = 'questions'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class SampleQuestionUpdateView(AjaxRequestMixin, LoginRequiredMixin, UpdateView):
    model = SampleQuestion
    template_name = "vw_question/edit_form.html"
    form_class = SampleQuestionForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        data = super(SampleQuestionUpdateView, self).get_context_data(**kwargs)
        if self.object.position:
            data.update({'position': self.object.position.name})
        if self.object.competency:
            data.update({'competency': self.object.competency.name})
        return data

    def form_valid(self, form):
        form_data = form.save(commit=False)
        form_data.user = self.request.user
        if self.request.POST.get('position'):
            role, _ = Position.objects.get_or_create(
                name=self.request.POST['position'],
                user=self.request.user
            )
            form_data.position = role
        else:
            form_data.position = None
        if self.request.POST.get('competency'):
            role, _ = Competency.objects.get_or_create(name=self.request.POST['competency'])
            form_data.competency = role
        else:
            form_data.competency = None
        form_data.save()
        return super(SampleQuestionUpdateView, self).form_valid(form)
