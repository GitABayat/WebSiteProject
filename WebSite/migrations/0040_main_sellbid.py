# Generated by Django 3.0.9 on 2022-06-18 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0039_auto_20220615_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='sellbid',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
    ]
