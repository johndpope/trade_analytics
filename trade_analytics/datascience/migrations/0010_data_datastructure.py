# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 05:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datascience', '0009_auto_20170720_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='DataStructure',
            field=models.CharField(choices=[('Channels', 'Channels'), ('Flattened', 'Flattened')], default='Channels', max_length=20),
        ),
    ]