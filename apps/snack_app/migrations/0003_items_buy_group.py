# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-25 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snack_app', '0002_auto_20180425_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='buy_group',
            field=models.ManyToManyField(related_name='items', to='snack_app.BuyGroup'),
        ),
    ]
