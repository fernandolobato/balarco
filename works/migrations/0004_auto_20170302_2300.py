# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-02 23:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0003_auto_20170301_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='status_id',
            field=models.IntegerField(choices=[(0, 'Pendiente'), (1, 'Diseño'), (2, 'Cuentas'), (3, 'Validación'), (4, 'Producción'), (5, 'Por cobrar'), (6, 'Por facturar'), (7, 'Terminado')]),
        ),
    ]