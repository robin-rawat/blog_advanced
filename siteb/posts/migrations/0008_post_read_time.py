# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-13 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20170612_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='read_time',
            field=models.IntegerField(default=0),
        ),
    ]