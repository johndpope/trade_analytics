# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-09 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0012_auto_20170509_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexcomputeclass',
            name='ClassName',
            field=models.CharField(help_text='Name of the index', max_length=100),
        ),
    ]
