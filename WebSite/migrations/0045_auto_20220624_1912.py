# Generated by Django 3.0.9 on 2022-06-24 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0044_auto_20220624_1907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cost',
            old_name='pricetype',
            new_name='takhfifpricetype',
        ),
    ]