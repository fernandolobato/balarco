# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-19 17:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('alternate_email', models.EmailField(max_length=255)),
                ('phone', models.CharField(max_length=50)),
                ('alternate_phone', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.Client')),
            ],
        ),
    ]
