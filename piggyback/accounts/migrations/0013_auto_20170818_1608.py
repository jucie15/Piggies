# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-18 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20170811_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, upload_to='%Y/%m/%d/profile/'),
        ),
    ]
