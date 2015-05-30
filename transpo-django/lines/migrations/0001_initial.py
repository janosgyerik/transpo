# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyScheduleDescriptor',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('days', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DailyScheduleTime',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('hour', models.IntegerField()),
                ('minute', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LineStation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('line', models.ForeignKey(to='lines.Line')),
            ],
        ),
        migrations.CreateModel(
            name='LineStationDailySchedule',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('priority', models.IntegerField()),
                ('descriptor', models.ForeignKey(to='lines.DailyScheduleDescriptor')),
                ('line', models.ForeignKey(to='lines.Line')),
            ],
        ),
        migrations.CreateModel(
            name='LineStationGenericSchedule',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date', models.DateTimeField()),
                ('line', models.ForeignKey(to='lines.Line')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='linestationgenericschedule',
            name='station',
            field=models.ForeignKey(to='lines.Station'),
        ),
        migrations.AddField(
            model_name='linestationdailyschedule',
            name='station',
            field=models.ForeignKey(to='lines.Station'),
        ),
        migrations.AddField(
            model_name='linestation',
            name='station',
            field=models.ForeignKey(to='lines.Station'),
        ),
        migrations.AddField(
            model_name='dailyscheduletime',
            name='schedule',
            field=models.ForeignKey(to='lines.LineStationDailySchedule'),
        ),
    ]
