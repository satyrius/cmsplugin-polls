# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_polls', '0002_poll_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='ends_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='poll',
            name='starts_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 2, 11, 33, 6, 830862), auto_now_add=True),
            preserve_default=False,
        ),
    ]
