# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncmxpof', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ncm',
            name='cod',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='pof',
            name='cod',
            field=models.BigIntegerField(),
        ),
    ]
