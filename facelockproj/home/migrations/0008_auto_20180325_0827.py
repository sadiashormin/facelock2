# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-25 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_post_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.ImageField(upload_to=b''),
        ),
    ]
