# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-06 18:17
from __future__ import unicode_literals

import core.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20160924_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='recurrences',
            field=core.fields.MoneypatchedRecurrenceField(blank=True, null=True),
        ),
    ]
