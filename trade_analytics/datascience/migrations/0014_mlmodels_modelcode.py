# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-04 04:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datascience', '0013_auto_20170803_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlmodels',
            name='ModelCode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datascience.ModelCode'),
        ),
    ]
