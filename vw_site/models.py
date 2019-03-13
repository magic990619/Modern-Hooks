# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from vw_candidate.models import Candidate


class InterviewToken(models.Model):
    candidate = models.ForeignKey(Candidate)
    token = models.CharField(max_length=50)
    expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "candidate: {0}".format(self.candidate)
