
from os import remove
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.db.models import Avg, Count, Max, Min, ProtectedError, Q, Sum, F
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.template.defaultfilters import date
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, View, ListView
from django.apps import apps
from django.contrib.auth import logout
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.decorators.csrf import csrf_exempt
from idpay.api import IDPayAPI 
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from .forms import *
from .models import *
from .serializers import *
import sys
from django.core import serializers

#----------------
#Public Functions
def str_to_class(str):
    return getattr(sys.modules[__name__], str)

#--------------------------
#Login And LogOut Functions

def logout_view(request):
    logout(request)
    request.session.get_expire_at_browser_close()
    request.session.clear_expired()
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()

    return redirect('WebSite:login')


#--------------------------------
#API ClassBaseViews (Serializers)

class ProductsListAPIView(ListAPIView):
    model = Products
    serializer_class = ProductsSerializers
    queryset = Products.objects.all()

#---------------
# CRUD Functions

@api_view(['POST'])
def Create(request):
    if request.method == 'POST':
        model_name = request.POST.get('model')
        RowID = request.POST.get('rowid', 0)        
        sn = request.POST.get('SerializersName')
        SerializersName = str_to_class(str(sn))
        result = SerializersName(data=request.data)
        if result.is_valid():
            result.save()
            if model_name == 'ProductsGroups' :
                if model_name == 'ProductsGroups' and int(RowID) != 0:
                    SelectedRow = ProductsGroups.objects.filter(id=int(RowID))
                    NewRow = ProductsGroups.objects.latest('id').id
                    if SelectedRow[0].gparentid == 0:
                        ProductsGroups.objects.filter(id=int(NewRow)).update(glevel=2, gparentid=int(RowID))
                    else:
                        ProductsGroups.objects.filter(id=int(NewRow)).update(glevel=3, gparentid=int(RowID))
                else:
                    NewRow = ProductsGroups.objects.latest('id').id
                    ProductsGroups.objects.filter(id=int(NewRow)).update(cparentid=0)
                    
            elif model_name == 'Productscategory':
                if model_name == 'Productscategory' and int(RowID) != 0:
                    SelectedRow = Productscategory.objects.filter(id=int(RowID))
                    NewRow = Productscategory.objects.latest('id').id
                    if SelectedRow[0].cparentid == 0:
                        Productscategory.objects.filter(id=int(NewRow)).update(cparentid=int(RowID))
                    else:
                        Productscategory.objects.filter(id=int(NewRow)).update(cparentid=int(RowID))
                else:
                    NewRow = Productscategory.objects.latest('id').id
                    Productscategory.objects.filter(id=int(NewRow)).update(cparentid=0)

            html = 'ok'
            data = {
                'html': html
            }
            return JsonResponse(data)
            
        html = result.errors
        if len(str(html)) > 0 :
            ErrorText = []
            for a in html:
                ErrorText.append('عملیات ایجاد به دلیل اشکال در پرکردن فیلد {field} با خطا متوقف گردید . متن سیسیتمی خطا : {ErrorResult}'.format(field=a, ErrorResult = str(html)))

        data = {
            'html': ErrorText
        }
        return JsonResponse(data)


@api_view(['GET'])
def getModelInfoForUpdate(request):
    model_name = request.GET.get('model')
    ModelName = apps.get_model('WebSite', model_name)
    RowID = request.GET.get('rowid')

    result = ModelName.objects.filter(id=RowID).values()
    data = {
        'result': result[0],
    }
    return JsonResponse(data)


@api_view(['POST'])
def Update(request):
    if request.method == 'POST':
        RowID = request.POST.get('rowid')
        model_name = request.POST.get('model')
        ModelName = apps.get_model('WebSite', model_name)
        UpdateResult = ModelName.objects.get(id=int(RowID))

        sn = request.POST.get('SerializersName')
        SerializersName = str_to_class(str(sn))
        
        result = SerializersName(UpdateResult, data=request.data)
        if result.is_valid():
            result.save()

            html = 'عملیات ویرایش با موفقیت انجام شد '
            data = {
            'html': html
            }
            return JsonResponse(data)
            
        html = result.errors
        if len(str(html)) > 0 :
            ErrorText = []
            for a in html:
                ErrorText.append('عملیات ویرایش به دلیل اشکال در پرکردن فیلد {field} با خطا متوقف گردید . متن سیسیتمی خطا : {ErrorResult}'.format(field=a, ErrorResult = str(html)))

        data = {
            'html': ErrorText
        }
        return JsonResponse(data)
    
             
def Delete(request):
    html = ''
    rowsid = request.GET.get('rowid', 0)
    ModelName = request.GET.get('model', 0)
    modelinfo = apps.get_model('WebSite', ModelName)

    modelinfo.objects.filter(id=int(rowsid)).delete()

    html = 'ردیف با کد {row} از سیستم حذف گردید .'.format(row=rowsid)
    data = {
        'html' : html
    }
    return JsonResponse(data)


def DeleteParametrs(request):
    html = ''
    Pid = request.GET.get('Pid', 0)
    ModelName = request.GET.get('model', 0)
    modelinfo = apps.get_model('WebSite', ModelName)

    modelinfo.objects.filter(Pid=int(Pid)).delete()

    html = 'کالای {row} از سیستم حذف گردید .'.format(row=Pid)
    data = {
        'html' : html
    }
    return JsonResponse(data)


#-----------------------------
# ListViews And DataTableViews 

# Products ListView And DTView Is Here:
class ProductsList(ListView):
    model = Products
    context_object_name = 'ProductsLV'
    template_name = 'ProductsAdminListView.html'
    queryset = Products.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductsList, self).get_context_data(**kwargs)
        context['groups'] = ProductsGroups.objects.all()
        context['group_parent_name'] = ProductsGroups.objects.all().filter(glevel=2) 
        context['group_parent_name_l1'] = ProductsGroups.objects.all().filter(glevel=1)
        context['cat'] = Productscategory.objects.all().filter(cparentid=0)

        file = open('/home/avashb/Projects/PY9.txt', 'r')
        py09 = []
        for info in file.read():
            py09.append(info)
        context['file'] = py09

        return context


class ProductsJsonDT(BaseDatatableView):
    model = Products
    columns = ['', '', 'id', 'name', 'serial', 'priceorg', 'group', 'sociallink', 'desc']

    def render_column(self, row, column):
        return super(ProductsJsonDT, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        
        if search:
            qs = qs.filter(Q(name__icontains=search)
             | Q(priceorg__contains=search)
             | Q(serial__contains=search)
             | Q(sociallink__icontains=search)
             | Q(desc_icontains=search))

        return qs


class CreateProductsParametrs(ListView):
    def get(self, request):
        RowID = request.GET.get('rowid', 0)
        Params = request.GET.get('chinput')
        paramlist = Params.split(',')
        errorhtml = ''

        CheckRowID = JoinPidAndParametrs.objects.filter(Pid=int(RowID))
        if len(CheckRowID) == 0:
            for a in paramlist:
                pd = Productscategory.objects.filter(cparentid=int(a), cparentid__gt = 0).values_list('id', 'cparentid', 'cname')
                if len(pd) > 0:
                    for lpd in pd:
                        if len(paramlist) == 1:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]),
                                Param0_Name=lpd[2])
                                p1.save()

                        if len(paramlist) == 2:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]),
                                Param0_Name=lpd[2])
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]),
                                    Param0_Name=b.Param0_Name, Param1_Name=lpd[2])
                                    p1.save()

                        if len(paramlist) == 3:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]),
                                Param0_Name=lpd[2])
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]),
                                    Param0_Name=b.Param0_Name, Param1_Name=lpd[2])
                                    p1.save()
                            elif int(paramlist[2]) and int(paramlist[2]) > 0 and int(paramlist[2]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), Param2=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level), 
                                    Param2_Level=int(lpd[1]), 
                                    Param0_Name=b.Param0_Name, Param1_Name=b.Param1_Name,
                                    Param2_Name=lpd[2])
                                    p2.save()

                        if len(paramlist) == 4:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]),
                                Param0_Name=lpd[1])
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]),
                                    Param0_Name=b.Param0_Name, Param1_Name=lpd[2])
                                    p1.save()
                            elif int(paramlist[2]) and int(paramlist[2]) > 0 and int(paramlist[2]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), Param2=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level), 
                                    Param2_Level=int(lpd[1]), 
                                    Param0_Name=b.Param0_Name, Param1_Name=b.Param1_Name,
                                    Param2_Name=lpd[2])
                                    p2.save()
                            elif int(paramlist[3]) and int(paramlist[3]) > 0 and int(paramlist[3]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0),
                                 Q(Param3=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), 
                                    Param2=int(b.Param2), Param3=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level),
                                    Param2_Level=int(b.Param2_Level), Param3_Level=int(lpd[1]),
                                    Param0_Name=b.Param0_Name, Param1_Name=b.Param1_Name,
                                    Param2_Name=b.Param2_Name, Param3_Name=lpd[2])
                                    p2.save()

                        if len(paramlist) == 5:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]),
                                Param0_Name=lpd[2])
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]),
                                    Param0_Name=b.Param0_Name, Param1_Name=lpd[2])
                                    p1.save()
                            elif int(paramlist[2]) and int(paramlist[2]) > 0 and int(paramlist[2]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), Param2=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level), 
                                    Param2_Level=int(lpd[1]), 
                                    Param0_Name=b.Param0_Name, Param1_Name=b.Param1_Name,
                                    Param2_Name=lpd[2])
                                    p2.save()
                            elif int(paramlist[3]) and int(paramlist[3]) > 0 and int(paramlist[3]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0),
                                 Q(Param3=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), 
                                    Param2=int(b.Param2), Param3=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level),
                                    Param2_Level=int(b.Param2_Level), Param3_Level=int(lpd[1]),
                                    Param0_Name=b.Param0_Name, Param1_Name=b.Param1_Name,
                                    Param2_Name=b.Param2_Name, Param3_Name=lpd[2])
                                    p2.save()
                            elif int(paramlist[4]) and int(paramlist[4]) > 0 and int(paramlist[4]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1),
                                    Param2=int(b.Param2), Param3=int(b.Param3), Param4=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(lpd[1]),
                                    Param0_Name=b.Param0_Name, Param1_Name=b.Param1_Name,
                                    Param2_Name=b.Param2_Name, Param3_Name=b.Param3_Name,
                                    Param4_Name=lpd[2])
                                    p2.save()

                        if len(paramlist) == 6:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]),
                                Param0_Name=lpd[2])
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]),
                                    Param0_Name=b.Param0_Name, Param1_Name=lpd[2])
                                    p1.save()
                            elif int(paramlist[2]) and int(paramlist[2]) > 0 and int(paramlist[2]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), Param2=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level), 
                                    Param2_Level=int(lpd[1]), 
                                    Param0_Name=b.Param0_Name, Param1_Name=b.Param1_Name,
                                    Param2_Name=lpd[2])
                                    p2.save()
                            elif int(paramlist[3]) and int(paramlist[3]) > 0 and int(paramlist[3]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0),
                                 Q(Param3=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), 
                                    Param2=int(b.Param2), Param3=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level),
                                    Param2_Level=int(b.Param2_Level), Param3_Level=int(lpd[1]),
                                    Param0_Name=b.Param0_Name, Param1_Name=b.Param1_Name,
                                    Param2_Name=b.Param2_Name, Param3_Name=lpd[2])
                                    p2.save()
                            elif int(paramlist[4]) and int(paramlist[4]) > 0 and int(paramlist[4]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1),
                                    Param2=int(b.Param2), Param3=int(b.Param3), Param4=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(lpd[1]),
                                    Param0_Name=b.Param0_Name, Param1_Name=b.Param1_Name,
                                    Param2_Name=b.Param2_Name, Param3_Name=b.Param3_Name,
                                    Param4_Name=lpd[2])
                                    p2.save()
                            elif int(paramlist[5]) and int(paramlist[5]) > 0 and int(paramlist[5]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(lpd[1]),
                                    Param0_Name=b.Param0_Name, Param1_Name=b.Param1_Name,
                                    Param2_Name=b.Param2_Name, Param3_Name=b.Param3_Name,
                                    Param4_Name=b.Param4_Name, Param5_Name=lpd[2]
                                    )
                                    p5.save()

                        
            if len(paramlist) == 2:           
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0)).delete()
            if len(paramlist) == 3:
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0)).delete()
            if len(paramlist) == 4:
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3=0)).delete()
            if len(paramlist) == 5:
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0)).delete()
            if len(paramlist) == 6:
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5=0)).delete()
            
        else:
            errorhtml = 'برای این کالا قبلا تعداد {rows} ردیف ایجاد شده است آیا مایل به ایجاد سایر ردیف ها هستید ؟'.format(rows=len(CheckRowID))

        html = 'ok'
        data = {
            'html': html,
            'rowid': RowID,
            'errorhtml': len(errorhtml),
            'texterrorhtml': errorhtml
        }
        return JsonResponse(data)


class ShowResultOfParamCreate(ListView):
    def get(self, request):
        RowID = request.GET.get('rowid')
        html = ''
        pr0__header_name = ''
        pr1__header_name = ''
        pr2__header_name = ''
        pr3__header_name = ''
        pr4__header_name = ''
        pr5__header_name = ''
        
        prheader_name = JoinPidAndParametrs.objects.filter(Pid=RowID).values_list('Param0_Level'
        ,'Param1_Level', 'Param2_Level', 'Param3_Level', 'Param4_Level', 'Param5_Level').first()

        if prheader_name != None:
            pr0__header_name = Productscategory.objects.get(id=int(prheader_name[0]), cparentid = 0).cname
            pr1__header_name = Productscategory.objects.get(id=int(prheader_name[1]), cparentid = 0).cname
            pr2__header_name = Productscategory.objects.get(id=int(prheader_name[2]), cparentid = 0).cname
            pr3__header_name = Productscategory.objects.get(id=int(prheader_name[3]), cparentid = 0).cname
            pr4__header_name = Productscategory.objects.get(id=int(prheader_name[4]), cparentid = 0).cname
            pr5__header_name = Productscategory.objects.get(id=int(prheader_name[5]), cparentid = 0).cname


            prlist = JoinPidAndParametrs.objects.filter(Pid=int(RowID)).values_list('Param0_Name','Param1_Name','Param2_Name','Param3_Name','Param4_Name','Param5_Name')
            product_name = Products.objects.get(id=int(RowID)).name
            for pr in prlist:
                html += """
                    <tr>\
                        <td><input type="text" class="d-inline fw-bold text-center form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{rowid}"></td>\
                        <td><input type="text" class="d-inline fw-bold text-center form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr0}"></td>\
                        <td><input type="text" class="d-inline fw-bold text-center form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr1}"></td>\
                        <td><input type="text" class="d-inline fw-bold text-center form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr2}"></td>\
                        <td><input type="text" class="d-inline fw-bold text-center form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr3}"></td>\
                        <td><input type="text" class="d-inline fw-bold text-center form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr4}"></td>\
                        <td><input type="text" class="d-inline fw-bold text-center form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr5}"></td>\
                        <td><input type="number" class="d-inline form-control fw-bold text-center col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value=""></td>\
                        <td><input type="number" class="d-inline form-control fw-bold text-center col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value=""></td>\
                    </tr>\
                    """.format(rowid=product_name, pr0=pr[0], pr1=pr[1], pr2=pr[2], pr3=pr[3], pr4=pr[4], pr5=pr[5])


        data = {
            'html': html,
            'prname0': pr0__header_name,
            'prname1': pr1__header_name,
            'prname2': pr2__header_name,
            'prname3': pr3__header_name,
            'prname4': pr4__header_name,
            'prname5': pr5__header_name
        }
        return JsonResponse(data)


# ProductsGroups ListView And DTView Is Here:
class ProductsGroupsList(ListView):
    model = ProductsGroups
    context_object_name = 'ProductsGroupsLV'
    template_name = 'ProductsGroupsAdminListView.html'
    queryset = ProductsGroups.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductsGroupsList, self).get_context_data(**kwargs)
        context['groups'] = ProductsGroups.objects.all()
        context['group_parent_name'] = ProductsGroups.objects.all().filter(glevel=2) 
        context['group_parent_name_l1'] = ProductsGroups.objects.all().filter(glevel=1)
        return context



class ProductsGroupsJsonDT(BaseDatatableView):
    model = ProductsGroups
    columns = ['', '', 'id', 'Group_Name', 'gparentid', 'glevel', 'GroupOrders', 'Group_Desc']

    def render_column(self, row, column):
        return super(ProductsGroupsJsonDT, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(Group_Name__icontains=search)
             | Q(glevel__contains=search)
             | Q(gparentid__contains=search)
             | Q(GroupOrders__contains=search)
             | Q(Group_Desc_icontains=search))

        qs = qs.filter(Q(gparentid = 0) , Q(id__gt = 0))
        return qs


class ProductsGroupsDetailJsonDT(BaseDatatableView):
    model = ProductsGroups
    columns = ['', '', 'id', 'Group_Name', 'gparentid', 'glevel', 'GroupOrders', 'Group_Desc']

    def render_column(self, row, column):
        return super(ProductsGroupsDetailJsonDT, self).render_column(row, column)

    def filter_queryset(self, qs):
        SubRowid = self.kwargs.get('rowid', 0)
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(Group_Name__icontains=search)
             | Q(glevel__contains=search)
             | Q(gparentid__contains=search)
             | Q(GroupOrders__contains=search)
             | Q(Group_Desc_icontains=search))

        qs = qs.filter(Q(gparentid = SubRowid) , Q(id__gt = 0))
        return qs


# ProductsCategory ListView And DTView Is Here:
class ProductsCategoryList(ListView):
    model = Productscategory
    context_object_name = 'ProductsCategoryList'
    template_name = 'ProductsCategoryAdminListView.html'
    queryset = Productscategory.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductsCategoryList, self).get_context_data(**kwargs)
        context['Category'] = Productscategory.objects.all()
        return context


class ProductsCategoryJsonDT(BaseDatatableView):
    model = Productscategory
    columns = ['', '', 'id', 'cname', 'cparentid', 'cdesc']

    def render_column(self, row, column):
        return super(ProductsCategoryJsonDT, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(cname__icontains=search)
             | Q(cparentid__contains=search)
             | Q(cdesc_icontains=search))

        qs = qs.filter(Q(cparentid = 0) , Q(id__gt = 0))
        return qs


class ProductsCategoryDetailJsonDT(BaseDatatableView):
    model = Productscategory
    columns = ['', '', 'id', 'cname', 'cparentid', 'cdesc']

    def render_column(self, row, column):
        return super(ProductsCategoryDetailJsonDT, self).render_column(row, column)

    def filter_queryset(self, qs):
        SubRowid = self.kwargs.get('rowid', 0)
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(cname__icontains=search)
             | Q(cparentid__contains=search)
             | Q(cdesc_icontains=search))

        qs = qs.filter(Q(cparentid = SubRowid) , Q(id__gt = 0))

        return qs
               
    
    