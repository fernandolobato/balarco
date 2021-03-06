# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-22 04:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_auto_20170221_0122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='alternate_phone',
            new_name='extension',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='phone',
            new_name='mobile_phone_2',
        ),
        migrations.AddField(
            model_name='contact',
            name='charge',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='landline',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='mobile_phone_1',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
