# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncmxpof', '0004_auto_20171128_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ncm',
            name='descript',
            field=models.CharField(max_length=900),
        ),
    ]