# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-13 16:05
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datascience', '0003_auto_20170624_0028'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataShard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ShardInfo', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='data',
            name='ShardInfo',
        ),
        migrations.AlterField(
            model_name='mlmodels',
            name='Status',
            field=models.CharField(choices=[('Validated', 'Validated'), ('Trained', 'Trained'), ('UnTrained', 'UnTrained'), ('Running', 'Running')], max_length=30),
        ),
        migrations.AddField(
            model_name='datashard',
            name='Data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datascience.Data'),
        ),
    ]