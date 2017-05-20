# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-20 02:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0013_auto_20170509_1249'),
        ('queryapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComputeStatus_Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(choices=[('ToDo', 'ToDo'), ('Run', 'Run'), ('Fail', 'Fail'), ('Success', 'Success')], max_length=10)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('Symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stockapp.Stockmeta')),
            ],
        ),
    ]