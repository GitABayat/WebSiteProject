# Generated by Django 3.0.9 on 2022-05-26 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0023_main'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellbascket',
            name='order_id',
            field=models.CharField(blank=True, default='0', max_length=128, null=True, verbose_name='ای دی سفارش'),
        ),
    ]
