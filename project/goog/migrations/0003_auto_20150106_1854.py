# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goog', '0002_auto_20150106_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]
