# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-26 02:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0010_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notif_type',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
