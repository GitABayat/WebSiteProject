# Generated by Django 3.0.9 on 2022-05-04 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0005_productscolors_productsparamerts_productssize'),
    ]

    operations = [
        migrations.AddField(
            model_name='productscolors',
            name='rgbacode',
            field=models.CharField(default=0, max_length=200, verbose_name='کد رنگ ار جی بی ا'),
        ),
        migrations.AlterField(
            model_name='productscolors',
            name='hezacode',
            field=models.CharField(default=0, max_length=200, verbose_name='کد رنگ هگزا'),
        ),
    ]
