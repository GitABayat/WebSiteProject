# Generated by Django 3.0.9 on 2022-06-24 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0043_cost_pricetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='pricetype',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=' روش تخفیف '),
        ),
        migrations.AlterField(
            model_name='cost',
            name='takhfiftype',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=' نوع تخفیف '),
        ),
    ]
