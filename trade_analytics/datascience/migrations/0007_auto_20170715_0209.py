# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-15 06:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datascience', '0006_computefunc_requiredgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.TextField(help_text=b'Code of all the features', null=True)),
                ('File', models.FilePathField(help_text=b'File of all the features', max_length=400, null=True)),
                ('Username', models.CharField(blank=True, help_text=b'User ID from database', max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModelCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.TextField(help_text=b'Code of all the features', null=True)),
                ('File', models.FilePathField(help_text=b'File of all the features', max_length=400, null=True)),
                ('Username', models.CharField(blank=True, help_text=b'User ID from database', max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='computefunc',
            name='Transformer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='data',
            name='TransfomerFunc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datascience.ComputeFunc'),
        ),
    ]