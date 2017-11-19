# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-19 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0003_longformset'),
    ]

    operations = [
        migrations.AddField(
            model_name='frame',
            name='createdat_string',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='frame',
            name='format_simple',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='frame',
            name='type_complex',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='frame',
            name='type_simple',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='frame',
            name='main_file',
            field=models.CharField(default='', max_length=300),
        ),
    ]
