# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unsplash', '0007_auto_20170123_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
