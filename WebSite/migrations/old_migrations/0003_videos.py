# Generated by Django 3.0.9 on 2021-04-22 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0002_auto_20210416_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videofile', models.FileField(upload_to='', verbose_name='فیلم')),
                ('Create_Date', models.DateTimeField(auto_now=True, null=True)),
                ('Update_Date', models.DateTimeField(auto_now_add=True, null=True)),
                ('Create_Uid', models.IntegerField(blank=True, default=0, null=True, verbose_name='کاربر ایجاد کننده')),
                ('Update_Uid', models.IntegerField(blank=True, default=0, null=True, verbose_name='کاربر ویرایش کننده')),
            ],
            options={
                'verbose_name': 'فیلم ',
                'verbose_name_plural': 'فیلم ها',
                'db_table': 'video',
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
    ]