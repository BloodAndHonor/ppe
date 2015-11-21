# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_date', models.DateField()),
                ('name', models.CharField(max_length=20)),
                ('number', models.CharField(max_length=20)),
                ('count', models.IntegerField()),
                ('unit', models.CharField(max_length=5)),
                ('old_location', models.CharField(max_length=20)),
                ('new_location', models.CharField(max_length=20)),
                ('old_user', models.CharField(max_length=10)),
                ('new_user', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('number', models.CharField(max_length=15, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('category_number', models.CharField(max_length=10)),
                ('model', models.CharField(max_length=50)),
                ('specification', models.CharField(max_length=50)),
                ('price', models.CharField(max_length=10)),
                ('vender', models.CharField(max_length=50)),
                ('buy_date', models.DateField()),
                ('status', models.CharField(max_length=15)),
                ('funds_category', models.CharField(max_length=15)),
                ('use_direction', models.CharField(max_length=15)),
                ('device_source', models.CharField(max_length=15)),
                ('use_person', models.CharField(max_length=10)),
                ('handby_person', models.CharField(max_length=10)),
                ('record_person', models.CharField(max_length=10)),
                ('input_person', models.CharField(max_length=10)),
                ('in_date', models.DateField()),
                ('document_number', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=20)),
                ('remarks', models.CharField(max_length=50)),
                ('funds_card', models.CharField(max_length=50)),
                ('user', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
