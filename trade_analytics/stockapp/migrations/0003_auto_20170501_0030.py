# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 04:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0002_auto_20170314_2022'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Watchlist',
            new_name='StockGroup',
        ),
    ]
