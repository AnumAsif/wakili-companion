# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-16 11:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.TextField()),
                ('plaintiff', models.TextField()),
                ('defendant', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CourtHearings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judge', models.TextField()),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Courts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HearingCases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField()),
                ('type', models.CharField(max_length=64)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courtlist.Cases')),
                ('hearing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='courtlist.CourtHearings')),
            ],
        ),
        migrations.CreateModel(
            name='Lawyers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='courthearings',
            name='court',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cause_list', to='courtlist.Courts'),
        ),
    ]
