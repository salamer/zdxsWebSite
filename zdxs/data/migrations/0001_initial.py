# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=80)),
                ('summury', models.CharField(max_length=300)),
                ('data_time', models.DateTimeField(auto_now_add=True)),
                ('editor', models.CharField(max_length=100)),
                ('data', models.TextField()),
                ('counts', models.IntegerField(default=0)),
                ('data_category', models.ForeignKey(to='data.Category')),
            ],
        ),
        migrations.CreateModel(
            name='DataComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('editor', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('data_time', models.DateTimeField(auto_now_add=True)),
                ('link', models.ForeignKey(to='data.Data')),
            ],
        ),
    ]
