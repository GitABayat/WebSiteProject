# Generated by Django 3.0.9 on 2022-06-23 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0040_main_sellbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalcheckout',
            name='sendtype',
            field=models.IntegerField(blank=True, choices=[(0, 'تحویل حضوری'), (1, 'ارسال با پیک'), (2, 'ارسال با پست پیش تاز')], default=0, null=True, verbose_name='روش ارسال'),
        ),
        migrations.AlterField(
            model_name='productsparamerts',
            name='takhfif',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='مبلغ پس از تخفیف'),
        ),
        migrations.AlterField(
            model_name='productsparamerts',
            name='takhfifprice',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='ملغ تخفیف'),
        ),
        migrations.AlterField(
            model_name='sellbascket',
            name='status',
            field=models.IntegerField(choices=[(0, 'سفارش'), (1, 'پرداخت شده'), (2, 'کنسل شده'), (3, 'درحال پرداخت')], default=0, verbose_name='وضعیت خرید'),
        ),
    ]