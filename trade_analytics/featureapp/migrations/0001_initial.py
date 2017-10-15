# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-01 02:46
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureComputeCode',
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
            name='FeaturesData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('T', models.DateField()),
                ('Symbol', models.CharField(blank=True, db_index=True, max_length=20, null=True)),
                ('Symbol_id', models.IntegerField(db_index=True, null=True)),
                ('Featuredata', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeaturesMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Featurelabel', models.CharField(help_text='unique label', max_length=50, unique=True)),
                ('FeatureFunction', models.CharField(help_text='function to compute the featurelabel', max_length=50, null=True)),
                ('Featuredescription', models.CharField(blank=True, help_text='Company name', max_length=100, null=True)),
                ('Category', models.CharField(blank=True, help_text='Company name', max_length=100, null=True)),
                ('Returntype', models.CharField(blank=True, help_text='Company name', max_length=100, null=True)),
                ('operators', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), blank=True, size=None)),
                ('Query', models.BooleanField(default=True, help_text='Use it in query')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('FeatureCode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='featureapp.FeatureComputeCode')),
            ],
        ),
    ]
