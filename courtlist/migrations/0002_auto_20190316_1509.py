# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-16 12:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courtlist', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hearingcases',
            old_name='type',
            new_name='hearing_type',
        ),
    ]
