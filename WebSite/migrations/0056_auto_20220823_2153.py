# Generated by Django 3.0.9 on 2022-08-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0055_productsparamerts_paramserial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='products',
            name='cname1',
        ),
        migrations.RemoveField(
            model_name='products',
            name='cname2',
        ),
        migrations.RemoveField(
            model_name='products',
            name='cname3',
        ),
        migrations.RemoveField(
            model_name='productsgroups',
            name='cname1',
        ),
        migrations.RemoveField(
            model_name='productsgroups',
            name='cname2',
        ),
        migrations.RemoveField(
            model_name='productsgroups',
            name='cname3',
        ),
        migrations.AlterField(
            model_name='productsparamerts',
            name='takhfifprice',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='مبلغ تخفیف'),
        ),
        migrations.DeleteModel(
            name='productsbrands',
        ),
    ]