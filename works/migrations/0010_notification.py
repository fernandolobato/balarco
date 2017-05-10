# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-21 14:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('works', '0009_file_filename'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('text', models.CharField(max_length=2000)),
                ('seen', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='works.Work')),
            ],
        ),
    ]