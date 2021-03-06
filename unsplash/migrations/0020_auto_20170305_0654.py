# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-05 06:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('unsplash', '0019_curatedlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curatedlist',
            name='curated_share_key',
        ),
        migrations.RemoveField(
            model_name='curatedlist',
            name='curated_user_id',
        ),
        migrations.AddField(
            model_name='curatedlist',
            name='curated_updated',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date updated'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='updated_at',
            field=models.DateTimeField(null=True, verbose_name='date updated'),
        ),
    ]
