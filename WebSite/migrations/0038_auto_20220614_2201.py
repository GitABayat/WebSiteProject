# Generated by Django 3.0.9 on 2022-06-14 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0037_auto_20220614_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsparaminvcharge',
            name='cid',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='invcid', to='WebSite.productscolors', verbose_name='رنگ'),
        ),
        migrations.AlterField(
            model_name='productsparaminvcharge',
            name='pid',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='invpid', to='WebSite.products', verbose_name='نام کالا'),
        ),
        migrations.AlterField(
            model_name='productsparaminvcharge',
            name='sid',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='invsid', to='WebSite.productssize', verbose_name='سایز'),
        ),
    ]
