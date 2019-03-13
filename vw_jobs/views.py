from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView, UpdateView, CreateView

from vw_jobs.forms import JobCreateForm
from vw_question.models import Position, SampleQuestion
from .models import Jobs, Questions


class JobListView(LoginRequiredMixin, ListView):
    template_name = 'vw_jobs/job_list.html'
    model = Jobs

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        user = self.request.user
        context.update({
            'positions': Position.objects.filter(user=user),
            'questions': SampleQuestion.objects.filter(user=user),
        })
        return context


class JobCreateView(LoginRequiredMixin, CreateView):
    template_name = 'vw_jobs/job_list.html'
    model = Jobs
    form_class = JobCreateForm

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'form': str(form)})

    def form_valid(self, form):
        form_data = form.save(commit=False)
        form_data.user = self.request.user
        protocol = 'https' if self.request.is_secure() else 'http'
        site_url = "{0}://{1}".format(
            protocol, self.request.META.get('HTTP_HOST', settings.SITE_URL)
        )
        form_data.link = "/".join([site_url, 'job', str(self.request.user.id), form_data.position])
        form_data.save()
        return JsonResponse({'status': 'ok', 'job_id': form_data.id})


class JobDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'vw_jobs/form_delete.html'
    model = Jobs

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'status': 'ok'})


class JobUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'vw_jobs/job_list.html'
    model = Jobs
    fields = '__all__'

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'form': form})

    def form_valid(self, form):
        super(JobUpdateView, self).form_valid(form)
        return JsonResponse({'status': 'ok'})


class JobQuestionCreateView(LoginRequiredMixin, CreateView):
    model = Questions
    template_name = 'vw_jobs/job_list.html'
    fields = '__all__'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(JobQuestionCreateView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        return JsonResponse({'status': 'error'})

    def form_valid(self, form):
        data_form = form.save(commit=False)
        if SampleQuestion.objects.filter(content__contains=data_form.question).exists():
            data_form.competency = SampleQuestion.objects.filter(
                content__contains=data_form.question
            ).first().competency
        data_form.save()

        return JsonResponse({'status': 'ok'})
