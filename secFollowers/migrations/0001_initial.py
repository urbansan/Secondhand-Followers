# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-19 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='secFollowersJson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.TextField(max_length=8)),
                ('csrf_token', models.TextField()),
                ('screen_name', models.CharField(max_length=20)),
                ('json', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TwittToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.TextField(max_length=8)),
                ('csrf_token', models.TextField()),
                ('utime', models.IntegerField()),
                ('is_authorized', models.BooleanField(default=False)),
                ('oauth_token', models.TextField()),
                ('oauth_token_secret', models.TextField()),
            ],
        ),
    ]
