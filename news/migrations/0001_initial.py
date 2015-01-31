# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='news',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.CharField(max_length=256)),
                ('url', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('pub_time', models.DateTimeField()),
                ('f_cutted', models.IntegerField(default=1)),
                ('publisher', models.ForeignKey(to='publisher.publisher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
