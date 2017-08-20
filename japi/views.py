from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, \
            Http404, HttpResponseForbidden
from django.core import serializers
from japi.models import *

# Create your views here.
@csrf_exempt
def index(request):
    return HttpResponse('hello')

@csrf_exempt
def get_products(request):
    all = Product.objects.all()
    json = serializers.serialize('json', all)
    return HttpResponse(json)

@csrf_exempt
def add_product(request):
    print(request.POST)
    print(request.body)
    print(request.is_ajax())
    name = request.POST.get('name', '')
    print("name: " + name)
    desc = request.POST.get('desc', '')
    if name:
        p = Product(name=name, desc=desc)
        p.save()
        return HttpResponse('success')
    else:
        raise Http404

@csrf_exempt
def disable_product(request):
    pk = request.POST.get('pk', '')
    if pk:
        p = Product.objects.get(pk=pk)
        if p:
            p.disable = True
            p.save()
            return HttpResponse('success')
        else:
            return HttpResponseNotFound('error')
    else:
        raise Http404