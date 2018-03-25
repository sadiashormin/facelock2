# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-25 08:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_face'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='face',
            name='id',
        ),
        migrations.AlterField(
            model_name='face',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
