# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-17 01:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170217_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(upload_to='media/profile_pictures'),
        ),
    ]
