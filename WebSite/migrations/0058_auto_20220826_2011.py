# Generated by Django 3.0.9 on 2022-08-26 15:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0005_auto_20220826_2011'),
        ('WebSite', '0057_joinpidandcid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baner1', models.ImageField(blank=True, null=True, upload_to='')),
                ('baner2', models.ImageField(blank=True, null=True, upload_to='')),
                ('baner3', models.ImageField(blank=True, null=True, upload_to='')),
                ('baner4', models.ImageField(blank=True, null=True, upload_to='')),
                ('baner5', models.ImageField(blank=True, null=True, upload_to='')),
                ('baner6', models.ImageField(blank=True, null=True, upload_to='')),
                ('baner7', models.ImageField(blank=True, null=True, upload_to='')),
                ('baner8', models.ImageField(blank=True, null=True, upload_to='')),
                ('baner9', models.ImageField(blank=True, null=True, upload_to='')),
                ('baner10', models.ImageField(blank=True, null=True, upload_to='')),
                ('baner11', models.ImageField(blank=True, null=True, upload_to='')),
                ('Create_Date', models.DateTimeField(auto_now=True)),
                ('Update_Date', models.DateTimeField(auto_now_add=True)),
                ('Create_Uid', models.IntegerField(blank=True, default=0, null=True)),
                ('Update_Uid', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'Banners',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.CreateModel(
            name='ContactUS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callinfo', models.CharField(blank=True, max_length=500, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('tell', models.CharField(blank=True, max_length=200, null=True)),
                ('tell2', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, max_length=200, null=True)),
                ('fax', models.CharField(blank=True, max_length=200, null=True)),
                ('internetsaletitle', models.CharField(blank=True, max_length=200, null=True)),
                ('internetsaledesc', models.TextField(blank=True, max_length=4000, null=True)),
                ('internetimg', models.ImageField(blank=True, null=True, upload_to='')),
                ('email', models.EmailField(blank=True, max_length=2000, null=True)),
                ('wtworkstart', models.CharField(blank=True, max_length=20, null=True)),
                ('wtworkend', models.CharField(blank=True, max_length=20, null=True)),
                ('ltworkstart', models.CharField(blank=True, max_length=20, null=True)),
                ('ltworkend', models.CharField(blank=True, max_length=20, null=True)),
                ('Create_Date', models.DateTimeField(auto_now=True)),
                ('Update_Date', models.DateTimeField(auto_now_add=True)),
                ('Create_Uid', models.IntegerField(blank=True, default=0, null=True)),
                ('Update_Uid', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'ContactUS',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.CreateModel(
            name='CustomersQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('tell', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('desc', models.CharField(max_length=2000)),
                ('Update_Date', models.DateTimeField(auto_now_add=True)),
                ('Create_Uid', models.IntegerField(blank=True, default=0, null=True)),
                ('Update_Uid', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'CustomersQuestions',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.CreateModel(
            name='JoinPidAndParametrs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pid', models.IntegerField(blank=True, default=0, null=True)),
                ('Param0', models.IntegerField(blank=True, default=0, null=True)),
                ('Param0_Level', models.IntegerField(choices=[(0, 'سطح 1'), (1, 'سطح 2'), (2, 'سطح 3'), (3, 'سطج 4'), (4, 'سطح 5'), (5, 'سطح 6'), (6, 'سطح 7'), (7, 'سطح 8'), (8, 'سطح 9'), (9, 'سطح 10')], default=0)),
                ('Param1', models.IntegerField(blank=True, default=0, null=True)),
                ('Param1_Level', models.IntegerField(blank=True, choices=[(0, 'سطح 1'), (1, 'سطح 2'), (2, 'سطح 3'), (3, 'سطج 4'), (4, 'سطح 5'), (5, 'سطح 6'), (6, 'سطح 7'), (7, 'سطح 8'), (8, 'سطح 9'), (9, 'سطح 10')], default=0, null=True)),
                ('Param2', models.IntegerField(blank=True, default=0, null=True)),
                ('Param2_Level', models.IntegerField(blank=True, choices=[(0, 'سطح 1'), (1, 'سطح 2'), (2, 'سطح 3'), (3, 'سطج 4'), (4, 'سطح 5'), (5, 'سطح 6'), (6, 'سطح 7'), (7, 'سطح 8'), (8, 'سطح 9'), (9, 'سطح 10')], default=0, null=True)),
                ('Param3', models.IntegerField(blank=True, default=0, null=True)),
                ('Param3_Level', models.IntegerField(blank=True, choices=[(0, 'سطح 1'), (1, 'سطح 2'), (2, 'سطح 3'), (3, 'سطج 4'), (4, 'سطح 5'), (5, 'سطح 6'), (6, 'سطح 7'), (7, 'سطح 8'), (8, 'سطح 9'), (9, 'سطح 10')], default=0, null=True)),
                ('Param4', models.IntegerField(blank=True, default=0, null=True)),
                ('Param4_Level', models.IntegerField(blank=True, choices=[(0, 'سطح 1'), (1, 'سطح 2'), (2, 'سطح 3'), (3, 'سطج 4'), (4, 'سطح 5'), (5, 'سطح 6'), (6, 'سطح 7'), (7, 'سطح 8'), (8, 'سطح 9'), (9, 'سطح 10')], default=0, null=True)),
                ('Param5', models.IntegerField(blank=True, default=0, null=True)),
                ('Param5_Level', models.IntegerField(blank=True, choices=[(0, 'سطح 1'), (1, 'سطح 2'), (2, 'سطح 3'), (3, 'سطج 4'), (4, 'سطح 5'), (5, 'سطح 6'), (6, 'سطح 7'), (7, 'سطح 8'), (8, 'سطح 9'), (9, 'سطح 10')], default=0, null=True)),
                ('Param6', models.IntegerField(blank=True, default=0, null=True)),
                ('Param6_Level', models.IntegerField(blank=True, choices=[(0, 'سطح 1'), (1, 'سطح 2'), (2, 'سطح 3'), (3, 'سطج 4'), (4, 'سطح 5'), (5, 'سطح 6'), (6, 'سطح 7'), (7, 'سطح 8'), (8, 'سطح 9'), (9, 'سطح 10')], default=0, null=True)),
                ('Param7', models.IntegerField(blank=True, default=0, null=True)),
                ('Param7_Level', models.IntegerField(blank=True, choices=[(0, 'سطح 1'), (1, 'سطح 2'), (2, 'سطح 3'), (3, 'سطج 4'), (4, 'سطح 5'), (5, 'سطح 6'), (6, 'سطح 7'), (7, 'سطح 8'), (8, 'سطح 9'), (9, 'سطح 10')], default=0, null=True)),
                ('Param8', models.IntegerField(blank=True, default=0, null=True)),
                ('Param8_Level', models.IntegerField(blank=True, choices=[(0, 'سطح 1'), (1, 'سطح 2'), (2, 'سطح 3'), (3, 'سطج 4'), (4, 'سطح 5'), (5, 'سطح 6'), (6, 'سطح 7'), (7, 'سطح 8'), (8, 'سطح 9'), (9, 'سطح 10')], default=0, null=True)),
                ('Param9', models.IntegerField(blank=True, default=0, null=True)),
                ('Param9_Level', models.IntegerField(blank=True, choices=[(0, 'سطح 1'), (1, 'سطح 2'), (2, 'سطح 3'), (3, 'سطج 4'), (4, 'سطح 5'), (5, 'سطح 6'), (6, 'سطح 7'), (7, 'سطح 8'), (8, 'سطح 9'), (9, 'سطح 10')], default=0, null=True)),
                ('ParamCount', models.IntegerField(blank=True, default=0, null=True)),
                ('ParamPrice', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'JoinPidAndParametrs',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.CreateModel(
            name='JoinPidAndPicturs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductID', models.CharField(default=0, max_length=200)),
                ('PImg', models.CharField(default=0, max_length=200)),
                ('Create_Date', models.DateTimeField(auto_now=True)),
                ('Update_Date', models.DateTimeField(auto_now_add=True)),
                ('Create_Uid', models.IntegerField(blank=True, default=0, null=True)),
                ('Update_Uid', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'JoinPidAndPicturs',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='')),
                ('Create_Date', models.DateTimeField(auto_now=True)),
                ('Update_Date', models.DateTimeField(auto_now_add=True)),
                ('Create_Uid', models.IntegerField(blank=True, default=0, null=True)),
                ('Update_Uid', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'Logo',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.CreateModel(
            name='MasterDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid_name', models.CharField(blank=True, default=0, max_length=256, null=True)),
                ('pid', models.IntegerField(blank=True, default=0, null=True)),
                ('gid_name', models.CharField(blank=True, default=0, max_length=256, null=True)),
                ('gid', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.BigIntegerField(blank=True, null=True, verbose_name='مبلغ تخفیف')),
                ('priceoffpercent', models.IntegerField(blank=True, default=0, null=True, verbose_name=' درصد تخفیف')),
                ('takhfiftype', models.BigIntegerField(blank=True, null=True, verbose_name='نوع تخفیف')),
                ('takhfifpricetype', models.BigIntegerField(blank=True, null=True, verbose_name='نوع مبلغ')),
                ('desc', models.TextField(blank=True, max_length=4000, null=True, verbose_name='توضیحات')),
                ('Create_Date', models.DateTimeField(auto_now=True)),
                ('Update_Date', models.DateTimeField(auto_now_add=True)),
                ('Create_Uid', models.IntegerField(blank=True, default=0, null=True)),
                ('Update_Uid', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'MasterDiscount',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.CreateModel(
            name='ProductsComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Head', models.TextField(blank=True, max_length=400, null=True)),
                ('com', models.TextField(blank=True, max_length=4000, null=True)),
                ('status', models.IntegerField(choices=[(0, 'پیش نویس'), (1, 'تایید شده'), (2, 'رد شده')], default=0)),
                ('Create_Date', models.DateTimeField(auto_now=True)),
                ('Update_Date', models.DateTimeField(auto_now_add=True)),
                ('Create_Uid', models.IntegerField(blank=True, default=0, null=True)),
                ('Update_Uid', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'ProductsComments',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.CreateModel(
            name='ProductsDiscounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Dmax_Type', models.IntegerField(choices=[(0, 'بدون روش'), (1, 'براساس مبلغ'), (2, 'براساس مقدار'), (3, 'براساس مبلغ و مقدار')], default=0)),
                ('DmaxPriceToSend', models.IntegerField(blank=True, default=0, null=True)),
                ('DmaxCountToSend', models.IntegerField(blank=True, default=0, null=True)),
                ('ErsalPrice', models.IntegerField(blank=True, default=0, null=True)),
                ('Create_Date', models.DateTimeField(auto_now=True)),
                ('Update_Date', models.DateTimeField(auto_now_add=True)),
                ('Create_Uid', models.IntegerField(blank=True, default=0, null=True)),
                ('Update_Uid', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'ProductsDiscounts',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.CreateModel(
            name='ProductsParametrs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paramserial', models.CharField(default=0, max_length=200, verbose_name='سریال کالا')),
                ('productinventory', models.CharField(default=0, max_length=200, verbose_name='تعداد اولیه')),
                ('productinventory_recharge', models.BigIntegerField(default=0, verbose_name='تعداد شارژ شده')),
                ('productinventory_sold', models.BigIntegerField(default=0, verbose_name='تعداد فروخته شده')),
                ('productinventory_remain', models.BigIntegerField(default=0, verbose_name='تعداد باقی مانده')),
                ('productprice', models.CharField(default=0, max_length=200, verbose_name='قیمت')),
                ('takhfif', models.FloatField(blank=True, default=0, null=True, verbose_name='مبلغ پس از تخفیف')),
                ('takhfifprice', models.FloatField(blank=True, default=0, null=True, verbose_name='مبلغ تخفیف')),
                ('pdesc', models.TextField(blank=True, default='', max_length=500, null=True, verbose_name='توضیح')),
                ('Param0', models.IntegerField(blank=True, default=0, null=True)),
                ('Param1', models.IntegerField(blank=True, default=0, null=True)),
                ('Param2', models.IntegerField(blank=True, default=0, null=True)),
                ('Param3', models.IntegerField(blank=True, default=0, null=True)),
                ('Param4', models.IntegerField(blank=True, default=0, null=True)),
                ('Param5', models.IntegerField(blank=True, default=0, null=True)),
                ('Param6', models.IntegerField(blank=True, default=0, null=True)),
                ('Param7', models.IntegerField(blank=True, default=0, null=True)),
                ('Param8', models.IntegerField(blank=True, default=0, null=True)),
                ('Param9', models.IntegerField(blank=True, default=0, null=True)),
                ('Create_Date', models.DateTimeField(auto_now=True)),
                ('Update_Date', models.DateTimeField(auto_now_add=True)),
                ('Create_Uid', models.IntegerField(blank=True, default=0, null=True, verbose_name='کاربر ایجاد کننده')),
                ('Update_Uid', models.IntegerField(blank=True, default=0, null=True, verbose_name='کاربر ویرایش کننده')),
            ],
            options={
                'db_table': 'ProductsParametrs',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.CreateModel(
            name='ProductsParamInvReCharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(blank=True, default=0, null=True)),
                ('Create_Date', models.DateTimeField(auto_now=True)),
                ('Update_Date', models.DateTimeField(auto_now_add=True)),
                ('Create_Uid', models.IntegerField(blank=True, default=0, null=True)),
                ('Update_Uid', models.IntegerField(blank=True, default=0, null=True)),
                ('paramid', models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='invpid', to='WebSite.ProductsParametrs')),
            ],
            options={
                'db_table': 'ProductsParamInvReCharge',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.CreateModel(
            name='ProductStars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(blank=True, null=True)),
                ('Create_Date', models.DateTimeField(auto_now=True)),
                ('Update_Date', models.DateTimeField(auto_now_add=True)),
                ('uid', models.IntegerField(verbose_name='کاربر')),
            ],
            options={
                'db_table': 'ProductStars',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.CreateModel(
            name='Sliders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Page_Selector', models.IntegerField(choices=[(0, 'صفحه اصلی'), (1, 'صفحه نمایش براساس گروه')], default=0)),
                ('FirstPage_Carousel_pic_1', models.ImageField(upload_to='', verbose_name='انتخاب عکس')),
                ('Create_Date', models.DateTimeField(auto_now=True, null=True)),
                ('Update_Date', models.DateTimeField(auto_now_add=True, null=True)),
                ('Create_Uid', models.IntegerField(blank=True, default=0, null=True, verbose_name='کاربر ایجاد کننده')),
                ('Update_Uid', models.IntegerField(blank=True, default=0, null=True, verbose_name='کاربر ویرایش کننده')),
            ],
            options={
                'db_table': 'Sliders',
                'ordering': ['id'],
                'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User')),
            },
        ),
        migrations.RenameModel(
            old_name='sellbascket',
            new_name='Buybasket',
        ),
        migrations.DeleteModel(
            name='aboutusp1',
        ),
        migrations.DeleteModel(
            name='Articls',
        ),
        migrations.DeleteModel(
            name='centercontactus',
        ),
        migrations.DeleteModel(
            name='Check',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='pid',
        ),
        migrations.RemoveField(
            model_name='commentdetails',
            name='cid',
        ),
        migrations.RemoveField(
            model_name='cost',
            name='pid',
        ),
        migrations.DeleteModel(
            name='customerquestions',
        ),
        migrations.DeleteModel(
            name='Customers',
        ),
        migrations.DeleteModel(
            name='DiscountFinal',
        ),
        migrations.RemoveField(
            model_name='firstpagebaners',
            name='group1',
        ),
        migrations.RemoveField(
            model_name='firstpagebaners',
            name='group10',
        ),
        migrations.RemoveField(
            model_name='firstpagebaners',
            name='group11',
        ),
        migrations.RemoveField(
            model_name='firstpagebaners',
            name='group2',
        ),
        migrations.RemoveField(
            model_name='firstpagebaners',
            name='group3',
        ),
        migrations.RemoveField(
            model_name='firstpagebaners',
            name='group4',
        ),
        migrations.RemoveField(
            model_name='firstpagebaners',
            name='group5',
        ),
        migrations.RemoveField(
            model_name='firstpagebaners',
            name='group6',
        ),
        migrations.RemoveField(
            model_name='firstpagebaners',
            name='group7',
        ),
        migrations.RemoveField(
            model_name='firstpagebaners',
            name='group8',
        ),
        migrations.RemoveField(
            model_name='firstpagebaners',
            name='group9',
        ),
        migrations.DeleteModel(
            name='firstpagelogo',
        ),
        migrations.DeleteModel(
            name='insideslider',
        ),
        migrations.DeleteModel(
            name='JoinPidAndCid',
        ),
        migrations.DeleteModel(
            name='lastnews',
        ),
        migrations.DeleteModel(
            name='mastertakhfif',
        ),
        migrations.DeleteModel(
            name='parametrsersal',
        ),
        migrations.DeleteModel(
            name='parametrsosool',
        ),
        migrations.DeleteModel(
            name='parametsaccounts',
        ),
        migrations.DeleteModel(
            name='parametssas',
        ),
        migrations.DeleteModel(
            name='parametssupport',
        ),
        migrations.DeleteModel(
            name='PayRcv',
        ),
        migrations.DeleteModel(
            name='PayRcvCheck',
        ),
        migrations.RemoveField(
            model_name='productdetails',
            name='pid',
        ),
        migrations.RemoveField(
            model_name='productsparamerts',
            name='cid',
        ),
        migrations.RemoveField(
            model_name='productsparamerts',
            name='pid',
        ),
        migrations.RemoveField(
            model_name='productsparamerts',
            name='sid',
        ),
        migrations.RemoveField(
            model_name='productsparaminvcharge',
            name='invcid',
        ),
        migrations.RemoveField(
            model_name='productsparaminvcharge',
            name='invpid',
        ),
        migrations.RemoveField(
            model_name='productsparaminvcharge',
            name='invsid',
        ),
        migrations.DeleteModel(
            name='salecontactus',
        ),
        migrations.DeleteModel(
            name='slider',
        ),
        migrations.DeleteModel(
            name='SPArticle',
        ),
        migrations.DeleteModel(
            name='SPFactor',
        ),
        migrations.RemoveField(
            model_name='stars',
            name='pid',
        ),
        migrations.DeleteModel(
            name='usersendtype',
        ),
        migrations.DeleteModel(
            name='weblog',
        ),
        migrations.AlterModelOptions(
            name='aboutus',
            options={'ordering': ['id'], 'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User'))},
        ),
        migrations.AlterModelOptions(
            name='buybasket',
            options={'ordering': ['id'], 'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User'))},
        ),
        migrations.AlterModelOptions(
            name='customersgroup',
            options={'ordering': ['id'], 'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User'))},
        ),
        migrations.AlterModelOptions(
            name='finalcheckout',
            options={'ordering': ['id'], 'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User'))},
        ),
        migrations.AlterModelOptions(
            name='main',
            options={'ordering': ['id'], 'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User'))},
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['id'], 'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User'))},
        ),
        migrations.AlterModelOptions(
            name='productscategory',
            options={'ordering': ['id'], 'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User'))},
        ),
        migrations.AlterModelOptions(
            name='productsgroups',
            options={'ordering': ['id'], 'permissions': (('can_read_private_section', 'administrator'), ('SubAdmin', 'SubAdmin'), ('user_watcher', 'User'))},
        ),
        migrations.RemoveField(
            model_name='products',
            name='desc_1',
        ),
        migrations.RemoveField(
            model_name='products',
            name='desc_2',
        ),
        migrations.RemoveField(
            model_name='products',
            name='desc_3',
        ),
        migrations.RemoveField(
            model_name='products',
            name='goods',
        ),
        migrations.RemoveField(
            model_name='products',
            name='guarantee',
        ),
        migrations.RemoveField(
            model_name='products',
            name='guaranteecount',
        ),
        migrations.RemoveField(
            model_name='products',
            name='img1',
        ),
        migrations.RemoveField(
            model_name='products',
            name='img2',
        ),
        migrations.RemoveField(
            model_name='products',
            name='img3',
        ),
        migrations.RemoveField(
            model_name='products',
            name='img4',
        ),
        migrations.RemoveField(
            model_name='products',
            name='img5',
        ),
        migrations.RemoveField(
            model_name='products',
            name='img6',
        ),
        migrations.RemoveField(
            model_name='products',
            name='img_desc_1',
        ),
        migrations.RemoveField(
            model_name='products',
            name='img_desc_2',
        ),
        migrations.RemoveField(
            model_name='products',
            name='img_desc_3',
        ),
        migrations.RemoveField(
            model_name='products',
            name='numberofgoods',
        ),
        migrations.RemoveField(
            model_name='products',
            name='specialcell',
        ),
        migrations.RemoveField(
            model_name='products',
            name='supportaftersale',
        ),
        migrations.RemoveField(
            model_name='products',
            name='supportaftersalecount',
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='Create_Uid',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='Update_Uid',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='personelimg',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='pposision',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='ptitle',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='buybasket',
            name='pid',
            field=models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.PROTECT, to='WebSite.Products', verbose_name='کد محصول'),
        ),
        migrations.AlterField(
            model_name='customersgroup',
            name='Create_Uid',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='customersgroup',
            name='Update_Uid',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='customersgroup',
            name='desc',
            field=models.CharField(blank=True, default='ندارد', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='customersgroup',
            name='name',
            field=models.CharField(default='ندارد', max_length=500),
        ),
        migrations.AlterField(
            model_name='finalcheckout',
            name='Create_Date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='finalcheckout',
            name='Update_Date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='finalcheckout',
            name='senddate',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='تاریخ ارسال'),
        ),
        migrations.AlterField(
            model_name='products',
            name='group',
            field=models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.PROTECT, to='WebSite.ProductsGroups', verbose_name='نام گروه'),
        ),
        migrations.AlterModelTable(
            name='aboutus',
            table='AboutUS',
        ),
        migrations.AlterModelTable(
            name='buybasket',
            table='Buybasket',
        ),
        migrations.AlterModelTable(
            name='customersgroup',
            table='CustomersGroup',
        ),
        migrations.AlterModelTable(
            name='finalcheckout',
            table='FinalCheckOut',
        ),
        migrations.AlterModelTable(
            name='products',
            table='Products',
        ),
        migrations.AlterModelTable(
            name='productscategory',
            table='Productscategory',
        ),
        migrations.AlterModelTable(
            name='productsgroups',
            table='ProductsGroups',
        ),
        migrations.DeleteModel(
            name='comment',
        ),
        migrations.DeleteModel(
            name='commentdetails',
        ),
        migrations.DeleteModel(
            name='cost',
        ),
        migrations.DeleteModel(
            name='firstpagebaners',
        ),
        migrations.DeleteModel(
            name='productdetails',
        ),
        migrations.DeleteModel(
            name='productscolors',
        ),
        migrations.DeleteModel(
            name='productsparamerts',
        ),
        migrations.DeleteModel(
            name='productsparaminvcharge',
        ),
        migrations.DeleteModel(
            name='productssize',
        ),
        migrations.DeleteModel(
            name='stars',
        ),
        migrations.AddField(
            model_name='productstars',
            name='pid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WebSite.Products'),
        ),
        migrations.AddField(
            model_name='productsparametrs',
            name='pid',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='WebSite.Products', verbose_name='نام کالا'),
        ),
        migrations.AddField(
            model_name='productscomments',
            name='pid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WebSite.Products'),
        ),
        migrations.AddField(
            model_name='masterdiscount',
            name='paramid',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='DscountParamid', to='WebSite.ProductsParametrs'),
        ),
        migrations.AddField(
            model_name='banners',
            name='group1',
            field=models.ForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group1', to='WebSite.ProductsGroups'),
        ),
        migrations.AddField(
            model_name='banners',
            name='group10',
            field=models.ForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group10', to='WebSite.ProductsGroups'),
        ),
        migrations.AddField(
            model_name='banners',
            name='group11',
            field=models.ForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group11', to='WebSite.ProductsGroups'),
        ),
        migrations.AddField(
            model_name='banners',
            name='group2',
            field=models.ForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group2', to='WebSite.ProductsGroups'),
        ),
        migrations.AddField(
            model_name='banners',
            name='group3',
            field=models.ForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group3', to='WebSite.ProductsGroups'),
        ),
        migrations.AddField(
            model_name='banners',
            name='group4',
            field=models.ForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group4', to='WebSite.ProductsGroups'),
        ),
        migrations.AddField(
            model_name='banners',
            name='group5',
            field=models.ForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group5', to='WebSite.ProductsGroups'),
        ),
        migrations.AddField(
            model_name='banners',
            name='group6',
            field=models.ForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group6', to='WebSite.ProductsGroups'),
        ),
        migrations.AddField(
            model_name='banners',
            name='group7',
            field=models.ForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group7', to='WebSite.ProductsGroups'),
        ),
        migrations.AddField(
            model_name='banners',
            name='group8',
            field=models.ForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group8', to='WebSite.ProductsGroups'),
        ),
        migrations.AddField(
            model_name='banners',
            name='group9',
            field=models.ForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group9', to='WebSite.ProductsGroups'),
        ),
    ]
