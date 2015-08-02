# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=80)),
                ('summury', models.CharField(max_length=300)),
                ('data_time', models.DateTimeField(auto_now_add=True)),
                ('editor', models.CharField(max_length=80)),
                ('body', models.TextField()),
                ('counts', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('commentator', models.CharField(max_length=80)),
                ('comment', models.TextField()),
                ('data_time', models.DateTimeField(auto_now_add=True)),
                ('link', models.ForeignKey(to='blog.Blog')),
            ],
        ),
    ]
