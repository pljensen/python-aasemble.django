# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-26 16:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


def add_initial_features(apps, schema_editor):
    Feature = apps.get_model("common", "Feature")
    Feature.objects.create(name='DUMMY_FEATURE_EVERYONE_HAS_BY_DEFAULT',
                           on_by_default=True, description='Dummy feature. On by default.')
    Feature.objects.create(name='DUMMY_FEATURE_NOONE_HAS_BY_DEFAULT',
                           on_by_default=False, description='Dummy feature. Off by default.')


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('on_by_default', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('users', models.ManyToManyField(related_name='features', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(add_initial_features)
    ]
