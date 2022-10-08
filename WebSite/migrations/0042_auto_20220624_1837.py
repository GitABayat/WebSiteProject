# Generated by Django 3.0.9 on 2022-06-24 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0041_auto_20220623_1152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cost',
            options={'ordering': ['id'], 'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')), 'verbose_name': 'تخفیف', 'verbose_name_plural': 'تخفیف ها'},
        ),
        migrations.RemoveField(
            model_name='cost',
            name='effdate',
        ),
        migrations.RemoveField(
            model_name='cost',
            name='priceoff',
        ),
        migrations.RemoveField(
            model_name='cost',
            name='priceorg',
        ),
        migrations.RemoveField(
            model_name='cost',
            name='specialcell',
        ),
        migrations.AddField(
            model_name='cost',
            name='colorid',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='کد رنگ'),
        ),
        migrations.AddField(
            model_name='cost',
            name='gid',
            field=models.BigIntegerField(blank=True, null=True, verbose_name=' کد گروه کالا'),
        ),
        migrations.AddField(
            model_name='cost',
            name='price',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='مبلغ تخفیف'),
        ),
        migrations.AddField(
            model_name='cost',
            name='priceoffpercent',
            field=models.CharField(default='0', max_length=4, verbose_name='درصد تخفیف'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cost',
            name='sizeid',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='کد سایز'),
        ),
        migrations.AddField(
            model_name='cost',
            name='takhfiftype',
            field=models.IntegerField(blank=True, null=True, verbose_name=' نوع تخفیف '),
        ),
        migrations.AlterField(
            model_name='cost',
            name='pid',
            field=models.BigIntegerField(blank=True, null=True, verbose_name=' کد کالا '),
        ),
    ]