# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_auto_20160109_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='factory_number',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
    ]
