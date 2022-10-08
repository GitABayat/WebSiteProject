
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

                pd = Productscategory.objects.filter(cparentid=int(a)).values_list('id', 'cparentid')
                if len(pd) > 0:
                    prname = []
                    for lpd in pd:
                        catinfo = Productscategory.objects.filter(id=lpd[0]).values_list('cname', 'id')
                        prname.append(catinfo)
                        if len(paramlist) == 1:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p0 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]))
                                p0.save()

                        if len(paramlist) == 2:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]))
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]), Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]))
                                    p1.save()

                        if len(paramlist) == 3:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]))
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]))
                                    p1.save()
                            elif int(paramlist[2]) and int(paramlist[2]) > 0 and int(paramlist[2]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level), 
                                    Param2_Level=int(lpd[1]))
                                    p2.save()

                        if len(paramlist) == 4:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]))
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]))
                                    p1.save()
                            elif int(paramlist[2]) and int(paramlist[2]) > 0 and int(paramlist[2]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), Param2=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level), Param2_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[3]) and int(paramlist[3]) > 0 and int(paramlist[3]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0),
                                 Q(Param3=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), 
                                    Param2=int(b.Param2), Param3=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level),
                                    Param2_Level=int(b.Param2_Level), Param3_Level=int(lpd[1]))
                                    p2.save()

                        if len(paramlist) == 5:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]))
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]))
                                    p1.save()
                            elif int(paramlist[2]) and int(paramlist[2]) > 0 and int(paramlist[2]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), Param2=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level), Param2_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[3]) and int(paramlist[3]) > 0 and int(paramlist[3]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0),
                                 Q(Param3=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), 
                                    Param2=int(b.Param2), Param3=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level),
                                    Param2_Level=int(b.Param2_Level), Param3_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[4]) and int(paramlist[4]) > 0 and int(paramlist[4]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1),
                                    Param2=int(b.Param2), Param3=int(b.Param3), Param4=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(lpd[1]))
                                    p2.save()

                        if len(paramlist) == 6:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]))
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]))
                                    p1.save()
                            elif int(paramlist[2]) and int(paramlist[2]) > 0 and int(paramlist[2]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), Param2=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level), Param2_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[3]) and int(paramlist[3]) > 0 and int(paramlist[3]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0),
                                 Q(Param3=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), 
                                    Param2=int(b.Param2), Param3=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level),
                                    Param2_Level=int(b.Param2_Level), Param3_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[4]) and int(paramlist[4]) > 0 and int(paramlist[4]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1),
                                    Param2=int(b.Param2), Param3=int(b.Param3), Param4=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[5]) and int(paramlist[5]) > 0 and int(paramlist[5]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(lpd[1]))
                                    p5.save()

                        if len(paramlist) == 7:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]))
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]))
                                    p1.save()
                            elif int(paramlist[2]) and int(paramlist[2]) > 0 and int(paramlist[2]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), Param2=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level), Param2_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[3]) and int(paramlist[3]) > 0 and int(paramlist[3]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0),
                                 Q(Param3=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), 
                                    Param2=int(b.Param2), Param3=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level),
                                    Param2_Level=int(b.Param2_Level), Param3_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[4]) and int(paramlist[4]) > 0 and int(paramlist[4]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1),
                                    Param2=int(b.Param2), Param3=int(b.Param3), Param4=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[5]) and int(paramlist[5]) > 0 and int(paramlist[5]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(lpd[1]))
                                    p5.save()
                            elif int(paramlist[6]) and int(paramlist[6]) > 0 and int(paramlist[6]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(b.Param5), Param6=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(b.Param5_Level), Param6_Level=int(lpd[1]))
                                    p5.save()

                        if len(paramlist) == 8:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]))
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]))
                                    p1.save()
                            elif int(paramlist[2]) and int(paramlist[2]) > 0 and int(paramlist[2]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), Param2=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level), Param2_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[3]) and int(paramlist[3]) > 0 and int(paramlist[3]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0),
                                 Q(Param3=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), 
                                    Param2=int(b.Param2), Param3=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level),
                                    Param2_Level=int(b.Param2_Level), Param3_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[4]) and int(paramlist[4]) > 0 and int(paramlist[4]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1),
                                    Param2=int(b.Param2), Param3=int(b.Param3), Param4=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[5]) and int(paramlist[5]) > 0 and int(paramlist[5]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(lpd[1]))
                                    p5.save()
                            elif int(paramlist[6]) and int(paramlist[6]) > 0 and int(paramlist[6]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(b.Param5), Param6=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(b.Param5_Level), Param6_Level=int(lpd[1]))
                                    p5.save()
                            elif int(paramlist[7]) and int(paramlist[7]) > 0 and int(paramlist[7]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6__gt=0), Q(Param7=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(b.Param5), Param6=int(b.Param6), 
                                    Param7=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(b.Param5_Level), Param6_Level=int(b.Param6_Level), 
                                    Param7_Level=int(lpd[1]))
                                    p5.save()

                        if len(paramlist) == 9:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]))
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]))
                                    p1.save()
                            elif int(paramlist[2]) and int(paramlist[2]) > 0 and int(paramlist[2]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), Param2=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level), Param2_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[3]) and int(paramlist[3]) > 0 and int(paramlist[3]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0),
                                 Q(Param3=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), 
                                    Param2=int(b.Param2), Param3=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level),
                                    Param2_Level=int(b.Param2_Level), Param3_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[4]) and int(paramlist[4]) > 0 and int(paramlist[4]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1),
                                    Param2=int(b.Param2), Param3=int(b.Param3), Param4=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[5]) and int(paramlist[5]) > 0 and int(paramlist[5]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(lpd[1]))
                                    p5.save()
                            elif int(paramlist[6]) and int(paramlist[6]) > 0 and int(paramlist[6]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(b.Param5), Param6=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(b.Param5_Level), Param6_Level=int(lpd[1]))
                                    p5.save()
                            elif int(paramlist[7]) and int(paramlist[7]) > 0 and int(paramlist[7]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6__gt=0), Q(Param7=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(b.Param5), Param6=int(b.Param6), 
                                    Param7=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(b.Param5_Level), Param6_Level=int(b.Param6_Level), 
                                    Param7_Level=int(lpd[1]))
                                    p5.save()
                            elif int(paramlist[8]) and int(paramlist[8]) > 0 and int(paramlist[8]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6__gt=0), Q(Param7__gt=0), Q(Param8=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(b.Param5), Param6=int(b.Param6), 
                                    Param7=int(b.Param7), Param8=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(b.Param5_Level), Param6_Level=int(b.Param6_Level), 
                                    Param7_Level=int(b.Param7_Level), Param8_Level=int(lpd[1]))
                                    p5.save()

                        if len(paramlist) == 10:
                            if int(paramlist[0]) and int(paramlist[0]) > 0 and int(paramlist[0]) == int(lpd[1]):
                                p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(lpd[0]), Param0_Level=int(lpd[1]))
                                p1.save()
                            elif int(paramlist[1]) and int(paramlist[1]) > 0 and int(paramlist[1]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0))
                                for b in a:
                                    p1 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(lpd[0]),
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(lpd[1]))
                                    p1.save()
                            elif int(paramlist[2]) and int(paramlist[2]) > 0 and int(paramlist[2]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), Param2=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level), Param2_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[3]) and int(paramlist[3]) > 0 and int(paramlist[3]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0),
                                 Q(Param3=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1), 
                                    Param2=int(b.Param2), Param3=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level), Param1_Level=int(b.Param1_Level),
                                    Param2_Level=int(b.Param2_Level), Param3_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[4]) and int(paramlist[4]) > 0 and int(paramlist[4]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0))
                                for b in a:
                                    p2 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), Param1=int(b.Param1),
                                    Param2=int(b.Param2), Param3=int(b.Param3), Param4=int(lpd[0]), 
                                    Param0_Level=int(b.Param0_Level),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(lpd[1]))
                                    p2.save()
                            elif int(paramlist[5]) and int(paramlist[5]) > 0 and int(paramlist[5]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), 
                                Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(lpd[1]))
                                    p5.save()
                            elif int(paramlist[6]) and int(paramlist[6]) > 0 and int(paramlist[6]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(b.Param5), Param6=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(b.Param5_Level), Param6_Level=int(lpd[1]))
                                    p5.save()
                            elif int(paramlist[7]) and int(paramlist[7]) > 0 and int(paramlist[7]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6__gt=0), Q(Param7=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(b.Param5), Param6=int(b.Param6), 
                                    Param7=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(b.Param5_Level), Param6_Level=int(b.Param6_Level), 
                                    Param7_Level=int(lpd[1]))
                                    p5.save()
                            elif int(paramlist[8]) and int(paramlist[8]) > 0 and int(paramlist[8]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6__gt=0), Q(Param7__gt=0), Q(Param8=0))
                                for b in a:
                                    p5 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(b.Param5), Param6=int(b.Param6), 
                                    Param7=int(b.Param7), Param8=int(lpd[0]),
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(b.Param5_Level), Param6_Level=int(b.Param6_Level), 
                                    Param7_Level=int(b.Param7_Level), Param8_Level=int(lpd[1]))
                                    p5.save()

                            elif int(paramlist[9]) and int(paramlist[9]) > 0 and int(paramlist[9]) == int(lpd[1]):
                                a = JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6__gt=0), Q(Param7__gt=0), Q(Param8__gt=0), Q(Param9=0))
                                for b in a:
                                    p8 = JoinPidAndParametrs(Pid=int(RowID), Param0=int(b.Param0), 
                                    Param1=int(b.Param1), Param2=int(b.Param2), Param3=int(b.Param3), 
                                    Param4=int(b.Param4), Param5=int(b.Param5), Param6=int(b.Param6), 
                                    Param7=int(b.Param7), Param8=int(b.Param8), Param9=int(lpd[0]), 
                                    Param1_Level=int(b.Param1_Level), Param2_Level=int(b.Param2_Level), 
                                    Param3_Level=int(b.Param3_Level), Param4_Level=int(b.Param4_Level),
                                    Param5_Level=int(b.Param5_Level), Param6_Level=int(b.Param6_Level), 
                                    Param7_Level=int(b.Param7_Level), Param8_Level=int(b.Param8_Level), 
                                    Param9_Level=int(lpd[1]))
                                    p8.save()

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
            if len(paramlist) == 7:
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6=0)).delete()
            if len(paramlist) == 8:
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6__gt=0), Q(Param7=0)).delete()
            if len(paramlist) == 9:
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6__gt=0), Q(Param7=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6__gt=0), Q(Param7__gt=0), Q(Param8=0)).delete()
            if len(paramlist) == 10:
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6__gt=0), Q(Param7=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6__gt=0), Q(Param7__gt=0), Q(Param8=0)).delete()
                JoinPidAndParametrs.objects.filter(Q(Pid=int(RowID)), Q(Param0__gt=0), Q(Param1__gt=0), Q(Param2__gt=0), Q(Param3__gt=0), Q(Param4__gt=0), Q(Param5__gt=0), Q(Param6__gt=0), Q(Param7__gt=0), Q(Param8__gt=0), Q(Param9=0)).delete()
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
        htmlheader = ''
        htmlfooter = ''
        param = JoinPidAndParametrs.objects.filter(Pid=RowID).order_by('Param0')
        for pr in param:
            pr0_name = Productscategory.objects.values('cname').filter(id=int(pr.Param0_Level)).first()
            pr1_name = Productscategory.objects.values('cname').filter(id=int(pr.Param1_Level)).first()
            pr2_name = Productscategory.objects.values('cname').filter(id=int(pr.Param2_Level)).first()
            pr3_name = Productscategory.objects.values('cname').filter(id=int(pr.Param3_Level)).first()
            pr4_name = Productscategory.objects.values('cname').filter(id=int(pr.Param4_Level)).first()
            pr5_name = Productscategory.objects.values('cname').filter(id=int(pr.Param5_Level)).first()
            pr6_name = Productscategory.objects.values('cname').filter(id=int(pr.Param6_Level)).first()
            pr7_name = Productscategory.objects.values('cname').filter(id=int(pr.Param7_Level)).first()
            pr8_name = Productscategory.objects.values('cname').filter(id=int(pr.Param8_Level)).first()
            pr9_name = Productscategory.objects.values('cname').filter(id=int(pr.Param9_Level)).first()
            if pr0_name:
                pr0__name = pr0_name['cname']
            else:
                pr0__name = 'پارامتر 0'
            if pr1_name:
                pr1__name = pr1_name['cname']
            else:
                pr1__name = 'پارامتر 1'
            if pr2_name:
                pr2__name = pr2_name['cname']
            else:
                pr2__name = 'پارامتر 2'
            if pr3_name:
                pr3__name = pr3_name['cname']
            else:
                pr3__name = 'پارامتر 3'       
            if pr4_name:
                pr4__name = pr4_name['cname']
            else:
                pr4__name = 'پارامتر 4' 
            if pr5_name:
                pr5__name = pr5_name['cname']
            else:
                pr5__name = 'پارامتر 5'        
            if pr6_name:
                pr6__name = pr6_name['cname']
            else:
                pr6__name = 'پارامتر 6'        
            if pr7_name:
                pr7__name = pr7_name['cname']
            else:
                pr7__name = 'پارامتر 7'        
            if pr8_name:
                pr8__name = pr8_name['cname']
            else:
                pr8__name = 'پارامتر 8'         
            if pr9_name:
                pr9__name = pr9_name['cname']
            else:
                pr9__name = 'پارامتر 9'

            htmlheader = """
            <div class="card ShowParamList" >\
                    <div class="card-body" style="overflow-y: auto; height: 300px">\
                        <table class="table table-striped table-bordered table-hover table-bg-light shadow text-dark fw-bold" style="width: 2048px; overflow-x: auto;">\
                            <thead>\
                                <tr>\
                                    <th class="text-center">کالا</th>\
                                    <th id="pr0nameHead" class="text-center">{prname0}</th>\
                                    <th id="pr1nameHead" class="text-center">{prname1}</th>\
                                    <th id="pr2nameHead" class="text-center">{prname2}</th>\
                                    <th id="pr3nameHead" class="text-center">{prname3}</th>\
                                    <th id="pr4nameHead" class="text-center">{prname4}</th>\
                                    <th id="pr5nameHead" class="text-center">{prname5}</th>\
                                    <th id="pr6nameHead" class="text-center">{prname6}</th>\
                                    <th id="pr7nameHead" class="text-center">{prname7}</th>\
                                    <th id="pr8nameHead" class="text-center">{prname8}</th>\
                                    <th id="pr9nameHead" class="text-center">{prname9}</th>\
                                    <th class="text-center">تعداد</th>\
                                    <th class="text-center">مبلغ</th>\
                                </tr>\
                            </thead>\
                            
                            """.format(
                                prname0 = pr0__name,
                                prname1 = pr1__name,
                                prname2 = pr2__name,
                                prname3 = pr3__name,
                                prname4 = pr4__name,
                                prname5 = pr5__name,
                                prname6 = pr6__name,
                                prname7 = pr7__name,
                                prname8 = pr8__name,
                                prname9 = pr9__name
                            )
            html += """
            <tbody>\
                <tr>\
                <td><input type="text" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{rowid}"></td>\
                <td><input type="text" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr0}"></td>\
                <td><input type="text" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr1}"></td>\
                <td><input type="text" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr2}"></td>\
                <td><input type="text" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr3}"></td>\
                <td><input type="text" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr4}"></td>\
                <td><input type="text" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr5}"></td>\
                <td><input type="text" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr6}"></td>\
                <td><input type="text" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr7}"></td>\
                <td><input type="text" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr8}"></td>\
                <td><input type="text" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value="{pr9}"></td>\
                <td><input type="number" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value=""></td>\
                <td><input type="number" class="d-inline form-control col-xl-2 col-lg-2 col-md-4 col-sm-6 col-xs-12" value=""></td>\
                     </tr>\
                    </tbody>\
            """.format(rowid=int(RowID), pr0=pr.Param0, pr1=pr.Param1, pr2=pr.Param2, pr3=pr.Param3,
                    pr4=pr.Param4, pr5=pr.Param5, pr6=pr.Param6, pr7=pr.Param7, pr8=pr.Param8, pr9=pr.Param9)

            htmlfooter = """
                    
                        </table>\
                    </div>\
                </div>\
            """
      
        
        data = {
            'htmlheader': htmlheader,
            'html': html,
            'htmlfooter': htmlfooter,
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
               
