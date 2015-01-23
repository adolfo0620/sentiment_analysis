# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Query', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='query_string',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
