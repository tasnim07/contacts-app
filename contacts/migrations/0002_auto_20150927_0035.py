# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_type', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=2)),
                ('postal_code', models.CharField(max_length=6)),
                ('contact', models.ForeignKey(to='contacts.Contact')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('contact', 'address_type')]),
        ),
    ]
