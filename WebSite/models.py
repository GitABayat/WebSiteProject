from django.db import models ,connection
from django.db.models.enums import Choices
from django.db.models.expressions import F
from django.template.defaultfilters import time
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from jdatetime import datetime
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Sliders(models.Model):
    pageselector = [
        (0, 'صفحه اصلی'),
        (1, 'صفحه نمایش براساس گروه')
    ]
    Page_Selector = models.IntegerField(default=0, choices=pageselector, null=False, blank=False)
    FirstPage_Carousel_pic_1 = models.ImageField(verbose_name='انتخاب عکس', null=False, blank=False)
    Create_Date = models.DateTimeField(auto_now=True, null=True, blank=True)
    Update_Date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Create_Uid = models.IntegerField(default=0, verbose_name=_('کاربر ایجاد کننده'), null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, verbose_name=_('کاربر ویرایش کننده'), null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'Sliders'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User')
        )

    def __str__(self):
        return str(self.Page_Selector)


class Productscategory(models.Model):
    cname = models.CharField(max_length=100, verbose_name=_('نام دسته بندی'), null=False, blank=False)
    cparentid = models.IntegerField(default=0, verbose_name=_('نام سطح بالادست'), null=True, blank=True)
    cdesc = models.TextField(max_length=100, verbose_name=_('شرح دسته بندی'), null=True, blank=True)
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, verbose_name=_(
        'کاربر ایجاد کننده'), null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, verbose_name=_(
        'کاربر ویرایش کننده'), null=True, blank=True)


    class Meta:
        ordering = ['id']
        db_table = 'Productscategory'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User')
        )

    def __str__(self):
        return str(self.cname)


class ProductsGroups(models.Model):

    group_orders = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10,'10'),
    ]
    GroupOrders = models.IntegerField(choices=group_orders, default=0, verbose_name=_('اولویت نمایش'), null=False, blank=False)
    gparentid = models.IntegerField(default=0, verbose_name=_('کد گروه سطح بالاتر'),null=True, blank=True)
    glevel = models.IntegerField(default=0, verbose_name=_('سطح گروه'), null=True, blank=True)
    group_img = models.ImageField(verbose_name=_('عکس گروه کالا'), null=True, blank=True )
    Group_Name = models.CharField(
        max_length=200, verbose_name=_('نام گروه'), null=True, blank=True)
    Group_Desc = models.TextField(max_length=4000, verbose_name=_(
        'توضیح گروه'), null=True, blank=True)
    
    Create_Date = models.DateTimeField(auto_now=True, null=True, blank=True)
    Update_Date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    Create_Uid = models.IntegerField(default=0, verbose_name=_(
        'کاربر ایجاد کننده'), null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, verbose_name=_(
        'کاربر ویرایش کننده'), null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'ProductsGroups'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User')
        )

    def __str__(self):
        return self.Group_Name


class Products(models.Model):

    name = models.CharField(max_length=200, verbose_name=_('نام محصول'), null=False, blank=False)
    group = models.ForeignKey(ProductsGroups, on_delete=models.PROTECT, max_length=200, verbose_name=_('نام گروه'),
                              null=False, blank=False)
    priceorg = models.BigIntegerField(default= 0, verbose_name=_('قیمت محصول'), null=True, blank=True)
    serial = models.CharField(max_length=200, verbose_name=_('شماره سریال'), null=True, blank=True, default=0)
    desc = models.TextField(max_length=4000, verbose_name=_(
        'توضیحات'), null=True, blank=True)
    sociallink = models.CharField(max_length=200, default='****', verbose_name=_('لینک شبکه اجتماعی'), null=True, blank=True)
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, verbose_name=_(
        'کاربر ایجاد کننده'), null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, verbose_name=_(
        'کاربر ویرایش کننده'), null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'Products'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User')
        )

    def __str__(self):
        return self.name


class JoinPidAndPicturs(models.Model):

    ProductID = models.CharField(default=0,max_length=200, null=False, blank=False)
    PImg = models.CharField(default=0,max_length=200, null=False, blank=False)
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'JoinPidAndPicturs'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User')
        )

    def __str__(self):
        return  self.ProductID

class JoinPidAndParametrs(models.Model):
    paramlevel = [
        (0, 'سطح 1'),
        (1, 'سطح 2'),
        (2, 'سطح 3'),
        (3, 'سطج 4'),
        (4, 'سطح 5'),
        (5, 'سطح 6'),
        (6, 'سطح 7'),
        (7, 'سطح 8'),
        (8, 'سطح 9'),
        (9, 'سطح 10'),
    ]
    Pid = models.IntegerField(default=0, null=True, blank=True)
    Param0 = models.IntegerField(default=0, null=True, blank=True)
    Param0_Level = models.IntegerField(default=0, choices=paramlevel, null=False, blank=False)
    Param1 = models.IntegerField(default=0, null=True, blank=True)
    Param1_Level = models.IntegerField(default=0, choices=paramlevel, null=True, blank=True)
    Param2 = models.IntegerField(default=0, null=True, blank=True)
    Param2_Level = models.IntegerField(default=0, choices=paramlevel, null=True, blank=True)
    Param3 = models.IntegerField(default=0, null=True, blank=True)
    Param3_Level = models.IntegerField(default=0, choices=paramlevel, null=True, blank=True)
    Param4 = models.IntegerField(default=0, null=True, blank=True)
    Param4_Level = models.IntegerField(default=0, choices=paramlevel, null=True, blank=True)
    Param5 = models.IntegerField(default=0, null=True, blank=True)
    Param5_Level = models.IntegerField(default=0, choices=paramlevel, null=True, blank=True)
    Param6 = models.IntegerField(default=0, null=True, blank=True)
    Param6_Level = models.IntegerField(default=0, choices=paramlevel, null=True, blank=True)
    Param7 = models.IntegerField(default=0, null=True, blank=True)
    Param7_Level = models.IntegerField(default=0, choices=paramlevel, null=True, blank=True)
    Param8 = models.IntegerField(default=0, null=True, blank=True)
    Param8_Level = models.IntegerField(default=0, choices=paramlevel, null=True, blank=True)
    Param9 = models.IntegerField(default=0, null=True, blank=True)
    Param9_Level = models.IntegerField(default=0, choices=paramlevel, null=True, blank=True)
    ParamCount = models.IntegerField(default=0, null=True, blank=True)
    ParamPrice = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'JoinPidAndParametrs'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User')
        )


class ProductsParametrs(models.Model):

    pid = models.ForeignKey(Products, default=0, on_delete=models.PROTECT,verbose_name=_('نام کالا'), null=False, blank=False)
    paramserial = models.CharField(default=0,max_length=200, verbose_name=_('سریال کالا'), null=False, blank=False)
    productinventory = models.CharField(default=0,max_length=200, verbose_name=_('تعداد اولیه'), null=False, blank=False)
    productinventory_recharge = models.BigIntegerField(default=0, verbose_name=_('تعداد شارژ شده'), null=False, blank=False)
    productinventory_sold = models.BigIntegerField(default=0, verbose_name=_('تعداد فروخته شده'), null=False, blank=False)
    productinventory_remain = models.BigIntegerField(default=0, verbose_name=_('تعداد باقی مانده'), null=False, blank=False)
    productprice = models.CharField(default=0,max_length=200, verbose_name=_('قیمت'), null=False, blank=False)
    takhfif = models.FloatField (default=0, verbose_name=_('مبلغ پس از تخفیف'), null=True, blank=True)
    takhfifprice = models.FloatField (default=0, verbose_name=_('مبلغ تخفیف'), null=True, blank=True)
    pdesc = models.TextField(max_length=500, default='', null=True, blank=True, verbose_name=_('توضیح'))
    Param0 = models.IntegerField(default=0, null=True, blank=True)
    Param1 = models.IntegerField(default=0, null=True, blank=True)
    Param2 = models.IntegerField(default=0, null=True, blank=True)
    Param3 = models.IntegerField(default=0, null=True, blank=True)
    Param4 = models.IntegerField(default=0, null=True, blank=True)
    Param5 = models.IntegerField(default=0, null=True, blank=True)
    Param6 = models.IntegerField(default=0, null=True, blank=True)
    Param7 = models.IntegerField(default=0, null=True, blank=True)
    Param8 = models.IntegerField(default=0, null=True, blank=True)
    Param9 = models.IntegerField(default=0, null=True, blank=True)
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, verbose_name=_('کاربر ایجاد کننده'), null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, verbose_name=_('کاربر ویرایش کننده'), null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'ProductsParametrs'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User')
        )

    def __str__(self):
        return str(self.pid) 


class ProductStars(models.Model):
    stars = models.IntegerField(null=True, blank=True)
    pid = models.ForeignKey(Products, on_delete=models.PROTECT, null=False, blank=False)
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    uid = models.IntegerField(verbose_name='کاربر')
    class Meta:
        ordering = ['id']
        db_table = 'ProductStars'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User'),
        )


class ProductsComments(models.Model):

    statustypes = [
        (0, 'پیش نویس'),
        (1, 'تایید شده'),
        (2, 'رد شده'),
    ]
    pid = models.ForeignKey(Products, on_delete=models.PROTECT, null=False, blank=False)
    Head = models.TextField(max_length=400, null=True, blank=True)
    com = models.TextField(max_length=4000, null=True, blank=True)
    status = models.IntegerField(choices=statustypes, default=0, null=False, blank=False)
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'ProductsComments'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User'),
        )

    def __str__(self):
        return str(self.pid)


class Buybasket(models.Model):
    statustypes = [
        (0, 'سفارش'),
        (1, 'پرداخت شده'),
        (2, 'کنسل شده'),
        (3, 'درحال پرداخت'),
    ]

    pid = models.ForeignKey(Products, on_delete=models.PROTECT, max_length=200, verbose_name=_('کد محصول'),null=False, blank=False)
    pgroupid = models.IntegerField(default=0, verbose_name=_('گروه کالا'), null=True, blank=True)
    pcount = models.IntegerField(default=1, verbose_name=_('تعداد کالا'), null=False, blank=False)
    price_after_off = models.BigIntegerField(default=1, verbose_name=_('مبلغ پس از تخفیف'), null=False, blank=False)
    pprise = models.BigIntegerField(default=0, verbose_name=_('قیمت کالا'), null=False, blank=False)
    pdiscount = models.BigIntegerField(default=0, verbose_name=_('تخیف کالا'), null=True, blank=True)
    status = models.IntegerField(choices=statustypes, default=0, verbose_name=_('وضعیت خرید'), null=False, blank=False)
    TrackingCode = models.BigIntegerField(default=0, verbose_name=_('کد رهگیری'), null=True, blank=True)
    colorid_bycolor = models.IntegerField(default=1, verbose_name=_('کد رنگ بر اساس رنگ'), null=True, blank=True)
    sizeid_bycolor = models.IntegerField(default=1, verbose_name=_('کد سایز بر اساس رنگ'), null=True, blank=True)
    colorid_bysize = models.IntegerField(default=1, verbose_name=_('کد رنگ بر اساس سایز'), null=True, blank=True)
    sizeid_bysize = models.IntegerField(default=1, verbose_name=_('کد سایز بر اساس سایز'), null=True, blank=True)
    orginalprice = models.BigIntegerField(default=0, verbose_name=_('قیمت اصلی کالا'), null=True, blank=True)
    order_id = models.CharField(max_length=128, default='0', verbose_name=_('ای دی سفارش'), null=True, blank=True)
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, verbose_name=_(
        'کاربر ایجاد کننده'), null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, verbose_name=_(
        'کاربر ویرایش کننده'), null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'Buybasket'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User'),
        )

    def __str__(self):
        return str(self.pid)


class FinalCheckOut(models.Model):
    statustypes = [
        (1, 'پرداخت شده'),
        (2, 'کنسل شده'),
    ]
    sent_status = [
        (0, 'ارسال نشده'),
        (1, 'ارسال شده'),
        (2, 'برگشت داده شده'),
    ]
    send_type = [
        (0, 'تحویل حضوری'),
        (1, 'ارسال با پیک'),
        (2, 'ارسال با پست پیش تاز'),
        
    ]
    senddate = models.DateField(default=timezone.datetime.now, verbose_name=_('تاریخ ارسال'), null=True, blank=True)
    sendstatus = models.IntegerField(choices=sent_status, default=0, verbose_name=_('وضعیت ارسال'), null=True, blank=True)
    postcode = models.CharField(max_length=128, default=0, verbose_name=_('کد مرسوله'), null=True, blank=True)
    sendtype = models.IntegerField(choices=send_type, default=0, verbose_name=_('روش ارسال'), null=True, blank=True)
    first_name = models.CharField(_('نام و نام خانوادگی'), max_length=100, blank=True, null=True)
    last_name = models.CharField(_('آدرس'), max_length=300, blank=True, null=True)
    cellphone = models.CharField(max_length=20, verbose_name=_('شماره موبایل کاربر'), blank=True, null=True) 
    email = models.EmailField(_('ایمیل'), blank=True, null=True)
    totalprise = models.IntegerField(default=0, verbose_name=_('مبلغ پرداخت شده'), null=True, blank=True) 
    TrackingCode = models.BigIntegerField(default=0, verbose_name=_('کد رهگیری'), null=True, blank=True)
    BankTrackingCode = models.BigIntegerField(default=0, verbose_name=_('کد رهگیری بانک '), null=True, blank=True)
    bank_card_no = models.CharField(max_length=20, verbose_name=_('شماره کارت بانکی مشتری'), blank=True, null=True) 
    status = models.IntegerField(choices=statustypes, default=0, verbose_name=_(
        'وضعیت خرید'), null=False, blank=False)
    colorid_bycolor = models.IntegerField(default=1, verbose_name=_('کد رنگ بر اساس رنگ'), null=True, blank=True)
    sizeid_bycolor = models.IntegerField(default=1, verbose_name=_('کد سایز بر اساس رنگ'), null=True, blank=True)
    colorid_bysize = models.IntegerField(default=1, verbose_name=_('کد رنگ بر اساس سایز'), null=True, blank=True)
    sizeid_bysize = models.IntegerField(default=1, verbose_name=_('کد سایز بر اساس سایز'), null=True, blank=True)
    order_id = models.CharField(max_length=128, default='0', verbose_name=_('ای دی سفارش'), null=True, blank=True)
    Create_Date = models.DateField(auto_now=True)
    Update_Date = models.DateField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, verbose_name=_(
        'کاربر ایجاد کننده'), null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, verbose_name=_(
        'کاربر ویرایش کننده'), null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'FinalCheckOut'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User')
        )

    def __int__(self):
        return self.totalprise


class Banners(models.Model):
    baner1 = models.ImageField(null=True, blank=True)
    group1 = models.ForeignKey(ProductsGroups,related_name='group1',on_delete=models.PROTECT, null=True, blank=True, default='0')
    baner2 = models.ImageField(null=True, blank=True)
    group2 = models.ForeignKey(ProductsGroups,related_name='group2',on_delete=models.PROTECT, null=True, blank=True, default='0')
    baner3 = models.ImageField(null=True, blank=True)
    group3 = models.ForeignKey(ProductsGroups,related_name='group3',on_delete=models.PROTECT, null=True, blank=True, default='0')
    baner4 = models.ImageField(null=True, blank=True)
    group4 = models.ForeignKey(ProductsGroups,related_name='group4',on_delete=models.PROTECT, null=True, blank=True, default='0')
    baner5 = models.ImageField(null=True, blank=True)
    group5 = models.ForeignKey(ProductsGroups,related_name='group5',on_delete=models.PROTECT, null=True, blank=True, default='0')
    baner6 = models.ImageField(null=True, blank=True)
    group6 = models.ForeignKey(ProductsGroups,related_name='group6',on_delete=models.PROTECT, null=True, blank=True, default='0')
    baner7 = models.ImageField(null=True, blank=True)
    group7 = models.ForeignKey(ProductsGroups,related_name='group7',on_delete=models.PROTECT, null=True, blank=True, default='0')
    baner8 = models.ImageField(null=True, blank=True)
    group8 = models.ForeignKey(ProductsGroups,related_name='group8',on_delete=models.PROTECT, null=True, blank=True, default='0')
    baner9 = models.ImageField(null=True, blank=True)
    group9 = models.ForeignKey(ProductsGroups,related_name='group9',on_delete=models.PROTECT, null=True, blank=True, default='0')
    baner10 = models.ImageField(null=True, blank=True)
    group10 = models.ForeignKey(ProductsGroups,related_name='group10',on_delete=models.PROTECT, null=True, blank=True, default='0')
    baner11 = models.ImageField(null=True, blank=True)
    group11 = models.ForeignKey(ProductsGroups,related_name='group11',on_delete=models.PROTECT, null=True, blank=True, default='0')
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'Banners'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User'),
        )

    def __str__(self):
        return self.baner1


class Logo(models.Model):

    logo = models.ImageField(null=False, blank=False)
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'Logo'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User'),
        )

    def __str__(self):
        return self.logo


class AboutUS(models.Model):

    personelimg = models.ImageField(null=False, blank=False)
    pposision = models.CharField(max_length=100, null=False, blank=False)
    ptitle = models.CharField(max_length=100, null=False, blank=False)
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'AboutUS'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User'),
        )

    def __str__(self):
        return str(self.pposision)


class ContactUS(models.Model):
    callinfo = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    tell = models.CharField(max_length=200, null=True, blank=True)
    tell2 = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    fax = models.CharField(max_length=200, null=True, blank=True)
    internetsaletitle = models.CharField(max_length=200, null=True, blank=True)
    internetsaledesc = models.TextField(max_length=4000, null=True, blank=True)
    internetimg = models.ImageField(null=True, blank=True)
    email = models.EmailField(max_length=2000, null=True, blank=True)
    wtworkstart = models.CharField(max_length=20, null=True, blank=True)
    wtworkend = models.CharField(max_length=20, null=True, blank=True)
    ltworkstart = models.CharField(max_length=20, null=True, blank=True)
    ltworkend = models.CharField(max_length=20, null=True, blank=True)  
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'ContactUS'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User'),
        )

    def __str__(self):
        return str(self.callinfo)


class CustomersQuestions(models.Model):

    name = models.CharField(max_length=500, null=False, blank=False)
    title = models.CharField(max_length=200, null=True, blank=True)
    tell = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    desc = models.CharField(max_length=2000, null=False, blank=False)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'CustomersQuestions'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User'),
        )

    def __str__(self):
        return str(self.name)



class CustomersGroup(models.Model):
    name = models.CharField(max_length=500, default='ندارد', null=False, blank=False)
    desc = models.CharField(max_length=500, default='ندارد', null=True, blank=True) 
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, null=True, blank=True)
        
    class Meta:
        ordering = ['id']
        db_table = 'CustomersGroup'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User'),
        )

    def __str__(self):
        return str(self.name)


class MasterUsers(User):
    avatar = models.FileField(blank=True, null=True)
    newpass =  models.CharField(max_length=100, blank=True, null=True)
    oldpassword =  models.CharField(max_length=100, blank=True, null=True)
    cellphone = models.CharField(max_length=11, blank=True, null=True)
    address =  models.CharField(max_length=500, blank=True, null=True)
    subscriptioncode =  models.CharField(max_length=20, blank=True, null=True)
    group = models.ForeignKey(CustomersGroup, on_delete=models.PROTECT, related_name='CGroup', null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'MasterUsers'
        permissions = (
          ('can_read_private_section', 'administrator'),
          ('SubAdmin', 'SubAdmin'),
          ('user_watcher', 'User'),
        )


class ProductsDiscounts(models.Model):
    
    DmaxType = [
        (0, 'بدون روش'),
        (1, 'براساس مبلغ'),
        (2, 'براساس مقدار'),
        (3, 'براساس مبلغ و مقدار')
    ]
    Dmax_Type = models.IntegerField(choices=DmaxType, default=0, null=False, blank=False)
    DmaxPriceToSend = models.IntegerField(default=0, null=True, blank=True)
    DmaxCountToSend = models.IntegerField(default=0, null=True, blank=True)
    ErsalPrice = models.IntegerField(default=0, null=True, blank=True)
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'ProductsDiscounts'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User'),
        )

    def __str__(self):
        return str(self.DmaxPriceToSend)


class Main(models.Model):
    order_id = models.TextField()
    payment_id = models.TextField()
    amount = models.IntegerField()
    date = models.TextField(default='-')
    card_number = models.TextField(default="****")
    idpay_track_id = models.BigIntegerField(default=0000)
    bank_track_id = models.TextField(default=0000)
    status = models.IntegerField(default=0)
    sellbid = models.TextField()
 
    class Meta:
        ordering = ['id']
        db_table = 'Main'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User'),
        )

    def __str__(self):
          return str(self.pk) + "  |   " + str(self.status)


class ProductsParamInvReCharge(models.Model):
    
    paramid = models.ForeignKey(ProductsParametrs, default=0, on_delete=models.PROTECT, related_name='invpid', null=False, blank=False)
    count = models.IntegerField(default=0, null=True, blank=True)
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'ProductsParamInvReCharge'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User')
        )



class MasterDiscount(models.Model):
    
    pid_name = models.CharField(max_length=256, default=0,null=True, blank=True)
    pid = models.IntegerField(default=0, null=True, blank=True)
    gid_name = models.CharField(max_length=256, default=0, null=True, blank=True)
    gid= models.IntegerField(default=0, null=True, blank=True)
    paramid = models.ForeignKey(ProductsParametrs, default=0, on_delete=models.PROTECT, related_name='DscountParamid', null=False, blank=False)
    price = models.BigIntegerField(verbose_name=_('مبلغ تخفیف'), null=True, blank=True)
    priceoffpercent = models.IntegerField(default=0,verbose_name=_(' درصد تخفیف'), null=True, blank=True)
    takhfiftype = models.BigIntegerField(verbose_name=_('نوع تخفیف'), null=True, blank=True)
    takhfifpricetype = models.BigIntegerField(verbose_name=_('نوع مبلغ'), null=True, blank=True)
    desc = models.TextField(max_length=4000, verbose_name=_('توضیحات'), null=True, blank=True)
    Create_Date = models.DateTimeField(auto_now=True)
    Update_Date = models.DateTimeField(auto_now_add=True)
    Create_Uid = models.IntegerField(default=0, null=True, blank=True)
    Update_Uid = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['id']
        db_table = 'MasterDiscount'
        permissions = (
            ('can_read_private_section', 'administrator'),
            ('SubAdmin', 'SubAdmin'),
            ('user_watcher', 'User')
        )

    def __str__(self):
        return str(self.pid_name)

