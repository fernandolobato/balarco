# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-24 01:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0007_auto_20170306_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='worktype',
            name='work_type_id',
            field=models.IntegerField(choices=[(0, 'Proyecto'), (1, 'Iguala'), (2, 'Graduación')], default=0),
            preserve_default=False,
        ),
    ]
