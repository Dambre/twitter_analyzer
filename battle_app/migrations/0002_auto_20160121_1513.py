# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-21 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='updated_time',
            field=models.DateTimeField(null=True),
        ),
    ]
