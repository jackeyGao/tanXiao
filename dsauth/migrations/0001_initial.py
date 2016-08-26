# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('duoshuo_id', models.IntegerField(default=0, serialize=False, primary_key=True)),
                ('username', models.CharField(default=b'', max_length=45)),
                ('token', models.IntegerField(default=0)),
                ('avatar', models.TextField(null=True, blank=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userprofile',
            unique_together=set([('duoshuo_id',)]),
        ),
    ]
