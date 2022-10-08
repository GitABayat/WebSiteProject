from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from WebSite.models import *



class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['name', 'group', 'priceorg', 'serial', 'sociallink', 'desc']


class ProductsGroupsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductsGroups
        fields = ['Group_Name', 'GroupOrders', 'Group_Desc']


class ProductsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Productscategory
        fields = ['cname', 'cdesc']






