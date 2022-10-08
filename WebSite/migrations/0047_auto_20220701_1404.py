# Generated by Django 3.0.9 on 2022-07-01 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0046_auto_20220624_2220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finalcheckout',
            name='colorid_bycolor',
        ),
        migrations.RemoveField(
            model_name='finalcheckout',
            name='colorid_bysize',
        ),
        migrations.RemoveField(
            model_name='finalcheckout',
            name='sizeid_bycolor',
        ),
        migrations.RemoveField(
            model_name='finalcheckout',
            name='sizeid_bysize',
        ),
        migrations.AddField(
            model_name='sellbascket',
            name='FactorNo',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name='شماره فاکتور'),
        ),
        migrations.AlterField(
            model_name='finalcheckout',
            name='postcode',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name='کد مرسوله'),
        ),
    ]