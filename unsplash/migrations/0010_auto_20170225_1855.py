# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-25 12:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unsplash', '0009_auto_20170225_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='photo_height',
            field=models.CharField(default='none', max_length=5),
        ),
        migrations.AddField(
            model_name='photo',
            name='photo_width',
            field=models.CharField(default='none', max_length=5),
        ),
        migrations.AddField(
            model_name='photo',
            name='user_profile_pic_small',
            field=models.URLField(default='none', null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='exif_aparture',
            field=models.CharField(default='none', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='exif_exposure',
            field=models.CharField(default='none', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='exif_focul',
            field=models.CharField(default='none', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='exif_iso',
            field=models.CharField(default='none', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='exif_make',
            field=models.CharField(default='none', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='exif_model',
            field=models.CharField(default='none', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='location_name',
            field=models.CharField(default='none', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo_category',
            field=models.CharField(default='none', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='user_profile_pic',
            field=models.URLField(default='none', null=True),
        ),
    ]
