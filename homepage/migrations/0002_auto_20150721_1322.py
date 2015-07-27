# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmodel',
            name='email',
            field=models.EmailField(max_length=75, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='contactmodel',
            name='message',
            field=models.TextField(verbose_name='Your Message'),
        ),
        migrations.AlterField(
            model_name='contactmodel',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
    ]
