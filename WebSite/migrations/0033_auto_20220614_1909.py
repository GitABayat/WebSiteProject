# Generated by Django 3.0.9 on 2022-06-14 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0032_productsparamerts_productinventory_recharge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsparamerts',
            name='productinventory_recharge',
            field=models.BigIntegerField(default=0, max_length=200, verbose_name='تعداد شارژ شده'),
        ),
    ]
