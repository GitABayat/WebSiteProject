# Generated by Django 3.0.9 on 2021-04-16 13:19

import datetime
from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='effdate',
            field=django_jalali.db.models.jDateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='تاریخ موثر'),
        ),
    ]
