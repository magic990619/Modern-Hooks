# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _


class Candidate(models.Model):
    """
    portrait - user avatar/photo
    position - the position to which the current candidate was interviewed
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    position = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    portrait = models.ImageField(upload_to='candidates', blank=True, null=True)
    resume = models.FileField(upload_to='resumes', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    subclient_group = models.ForeignKey(
        'vw_client_groups.SubClientGroup', verbose_name=_('SubClient Group'), null=True, blank=True
    )
    client_group = models.ForeignKey(
        'vw_client_groups.ClientGroup', verbose_name=_('Client Group'), null=True, blank=True
    )
    invite_message = models.TextField(_('Invite message'))

    def full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def __str__(self):
        return self.email

    @property
    def avg_rate(self):
        """
        property for counting  Average Rating in stars
        :return: float, the rating: x.0 || x.5 || (x+1).0
        """
        list_rates = list(
            self.question_set.filter(recording__rating__rate__isnull=False).
                values_list('recording__rating__rate', flat=True)
        )
        if list_rates:
            sum_rating = sum(list_rates)
            qty_rates = len(list_rates)
            rate = round(sum_rating / float(qty_rates), 2)
            if (rate % 1) < 0.25:
                return rate // 1
            elif (rate % 1) > 0.75:
                return (rate // 1) + 1
            else:
                return (rate // 1) + 0.5
        else:
            return 0.0

    @property
    def avg_rate_num(self):
        """
        property for counting  Average Rating
        :return: float
        """
        list_rates = list(
            self.question_set.filter(recording__rating__rate__isnull=False).
                values_list('recording__rating__rate', flat=True)
        )
        if list_rates:
            sum_rating = sum(list_rates)
            qty_rates = len(list_rates)
            return round(sum_rating / float(qty_rates), 2)
        else:
            return 0.0

    @property
    def avg_by_competency(self):
        return self.question_set.values('competency').annotate(rate=Avg('recording__rating__rate'))

    @property
    def list_users(self):
        rating_ids = self.question_set.all().values_list('recording__rating__id', flat=True)
        return Rating.objects.filter(id__in=rating_ids).distinct('user')


class Question(models.Model):
    """
    ques - text of question
    limit - max time that given for an answer
    competency - kind of professional activity for which characterizes the issue
    """
    candidate = models.ForeignKey(Candidate)
    ques = models.CharField(max_length=1000)
    limit = models.FloatField(default=5)
    order = models.IntegerField()
    competency = models.CharField(max_length=255, null=True)

    def __str__(self):
        return '{0} - {1}'.format(self.candidate, self.ques)


class Recording(models.Model):
    question = models.OneToOneField(Question)
    video = models.FileField(upload_to='recordings')

    def __str__(self):
        return 'video for {0}'.format(self.question)


class Rating(models.Model):
    rate = models.IntegerField(default=0)
    recording = models.ForeignKey(Recording)
    user = models.ForeignKey(get_user_model())

    def __str__(self):
        return ' - '.join([self.user.email, str(self.rate)])


@receiver(pre_delete, sender=Candidate)
def candidate_delete(sender, instance, **kwargs):
    instance.portrait.delete(False)
    instance.resume.delete(False)


@receiver(pre_delete, sender=Recording)
def recording_delete(sender, instance, **kwargs):
    instance.video.delete(False)
