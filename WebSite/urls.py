from django.urls import path, re_path
from . import views
from django.views.generic import TemplateView
from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'WebSite'
urlpatterns = [
    #ClassBaseViews Urls .
    path('ProductsGroupsList/', views.ProductsGroupsList.as_view(), name='ProductsGroupsList'),
    path('ProductsGroupsDetailJsonDT/<str:rowid>/', views.ProductsGroupsDetailJsonDT.as_view(), name='ProductsGroupsDetailJsonDT'),
    path('ProductsCategoryList/', views.ProductsCategoryList.as_view(), name='ProductsCategoryList'),
    path('ProductsCategoryDetailJsonDT/<str:rowid>/', views.ProductsCategoryDetailJsonDT.as_view(), name='ProductsCategoryDetailJsonDT'),
    path('ProductsList/', views.ProductsList.as_view(), name='ProductsList'),
    #DataTables Urls (In partials/link.html).
    path('ProductsGroupsJsonDT/', views.ProductsGroupsJsonDT.as_view(), name='ProductsGroupsJsonDT'),
    path('ProductsCategoryJsonDT/', views.ProductsCategoryJsonDT.as_view(), name='ProductsCategoryJsonDT'),
    path('ProductsJsonDT/', views.ProductsJsonDT.as_view(), name='ProductsJsonDT'),

    #Create & Update & Delete With RestFreamWork Syntax Urls .
    path('Create/', views.Create, name='Create'),
    path('Delete/', views.Delete, name='Delete'),
    path('Delete/AllParametrs/', views.DeleteParametrs, name='DeleteParametrs'),
    path('Update/', views.Update, name='Update'),

    path('CreateProductsParametrs/', views.CreateProductsParametrs.as_view(), name='CreateProductsParametrs'),
    path('ShowResultOfParamCreate/', views.ShowResultOfParamCreate.as_view(), name='ShowResultOfParamCreate'),
    #Show Rows Info For Update Urls In DataTables .
    path('getModelInfoForUpdate/', views.getModelInfoForUpdate, name='getModelInfoForUpdate'),
    #API Urls .
    path('ProductsListAPIView/', views.ProductsListAPIView.as_view(), name='ProductsListAPIView')
]

urlpatterns += [
    path('captcha/', include('captcha.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)