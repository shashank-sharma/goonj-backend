# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-08 20:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_online',
            field=models.BooleanField(default=False, verbose_name='online'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_activity',
            field=models.DateTimeField(default=datetime.date.today, verbose_name='last activity'),
        ),
    ]
