# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-26 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vw_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewtoken',
            name='expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
