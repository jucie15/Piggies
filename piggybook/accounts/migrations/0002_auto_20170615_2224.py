# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 13:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tag',
            field=tagging.fields.TagField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
