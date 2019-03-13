# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import AbstractUser, Permission
from django.db import models

from vw_client_groups.models import ClientGroup


class CustomizedUser(AbstractUser):
    email = models.EmailField()

    username = models.CharField(max_length=100, unique=True)

    client_group = models.ForeignKey(
        ClientGroup, on_delete=models.CASCADE, null=True, blank=True,
        related_name="client_group"
    )

    def __str__(self):
        data = []
        if self.first_name:
            data.append(self.first_name)
        if self.last_name:
            data.append(self.last_name)
        if len(data) == 2:
            return "{0} {1}".format(*data)
        elif len(data) == 0:
            return self.email
        else:
            return str(data[0])

    def save(self, *args, **kwargs):
        super(CustomizedUser, self).save(*args, **kwargs)
        permissions = ['add_subclientgroup', 'change_subclientgroup', 'delete_subclientgroup']
        if self.client_group:
            CustomizedUser.objects.filter(id=self.id).update(is_staff=True)
            for perm in Permission.objects.filter(codename__in=permissions):
                perm.user_set.add(self)
                perm.save()
        else:
            for perm in Permission.objects.filter(codename__in=permissions):
                self.user_permissions.remove(perm)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    parent_user = models.ForeignKey('self', on_delete=models.CASCADE, blank=True)
    position = models.CharField(max_length=50)


class InviteTemplate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    html = models.CharField(max_length=10000)
    is_global = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
