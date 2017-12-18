# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-17 23:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0005_auto_20171204_0732'),
    ]

    operations = [
        migrations.AddField(
            model_name='allterms',
            name='createdat',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='allterms',
            name='start_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='allterms',
            name='user_parent',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ingestion.Mind'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='termset',
            name='createdat',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='termset',
            name='rough_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='termset',
            name='user_parent',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ingestion.Mind'),
            preserve_default=False,
        ),
    ]