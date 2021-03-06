# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-05 06:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unsplash', '0018_devicedata_unique_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuratedList',
            fields=[
                ('curated_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('curated_title', models.CharField(max_length=200)),
                ('curated_description', models.CharField(max_length=500)),
                ('curated_published', models.DateTimeField(verbose_name='date published')),
                ('curated_is_curated', models.CharField(default=False, max_length=30)),
                ('curated_is_featured', models.CharField(default=False, max_length=30)),
                ('curated_total_photos', models.CharField(default=0, max_length=4)),
                ('curated_share_key', models.CharField(default='null', max_length=50)),
                ('curated_user_id', models.CharField(max_length=50)),
                ('curated_user_name', models.CharField(max_length=30)),
                ('curated_profile_image_small', models.URLField(default='none', null=True)),
                ('curated_profile_image_large', models.URLField(default='none', null=True)),
                ('curated_collection_url_self', models.URLField()),
                ('curated_collection_url_html', models.URLField()),
                ('curated_cover_photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unsplash.Photo')),
            ],
        ),
    ]
