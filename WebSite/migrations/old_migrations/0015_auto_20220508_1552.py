# Generated by Django 3.0.9 on 2022-05-08 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0014_auto_20220508_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsparamerts',
            name='bid',
            field=models.ForeignKey(default='NULL', on_delete=django.db.models.deletion.PROTECT, to='WebSite.productsbrands', verbose_name='برند'),
        ),
    ]
