# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-15 03:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smap', '0002_sumari_good'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sumari',
            name='lat',
            field=models.DecimalField(decimal_places=8, max_digits=12),
        ),
        migrations.AlterField(
            model_name='sumari',
            name='lng',
            field=models.DecimalField(decimal_places=8, max_digits=12),
        ),
    ]