# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-11 19:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=250)),
                ('moderated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='JoinedEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Squadup.Event')),
            ],
        ),
        migrations.CreateModel(
            name='ReportedUsers',
            fields=[
                ('incident_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=1000)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Squadup.User')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Squadup.User')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='reportedusers',
            name='reported_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reported_by', to='Squadup.User'),
        ),
        migrations.AddField(
            model_name='reportedusers',
            name='reported_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_id', to='Squadup.User'),
        ),
        migrations.AddField(
            model_name='joinedevents',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Squadup.User'),
        ),
        migrations.AddField(
            model_name='event',
            name='host_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Squadup.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Squadup.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Squadup.Event'),
        ),
        migrations.AddField(
            model_name='reportedusers',
            name='moderated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Squadup.Moderator'),
        ),
    ]
