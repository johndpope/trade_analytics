# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-01 03:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0013_auto_20170509_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, db_index=True, help_text='Stock Sector', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, db_index=True, help_text='Stock Sector', max_length=100, null=True)),
            ],
        ),
    ]
