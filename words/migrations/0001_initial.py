# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='words',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=256)),
                ('count', models.IntegerField(default=0)),
                ('wordtype', models.CharField(max_length=10)),
                ('parse_time', models.DateTimeField()),
                ('news_id', models.ForeignKey(to='news.news')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
