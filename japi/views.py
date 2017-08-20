from django.core import serializers
from django.db import transaction
from django.http import (Http404, HttpResponse, HttpResponseForbidden,
                         HttpResponseNotFound, HttpResponseServerError)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from japi.models import *


# Create your views here.
@csrf_exempt
def index(request):
    return HttpResponse('hello')

@csrf_exempt
def get_products(request): #todo: batch
    all = Product.objects.all()
    json = serializers.serialize('json', all)
    return HttpResponse(json)

@csrf_exempt
def add_product(request):
    name = request.POST.get('name', '')
    desc = request.POST.get('desc', '')
    if name:
        p = Product(name=name, desc=desc)
        p.save()
        return HttpResponse('success')
    else:
        raise Http404

@csrf_exempt
def update_product(request):
    pk = request.POST.get('pk', '')
    name = request.POST.get('name', '')
    desc = request.POST.get('desc', '')
    if pk and name:
        p = Product.objects.get(pk=pk)
        p.name = name
        p.desc = desc
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

@csrf_exempt
def get_shops(request): #todo: batch
    all = Shop.objects.all()
    json = serializers.serialize('json', all)
    return HttpResponse(json)

@csrf_exempt
def add_shop(request):
    name = request.POST.get('name', '')
    owner = request.POST.get('owner', '')
    phone = request.POST.get('phone', '')
    address = request.POST.get('address', '')
    position = request.POST.get('position', '')
    desc = request.POST.get('desc', '')
    if name:
        s = Shop(name=name, owner=owner, phone=phone, address=address, position=position, desc=desc)
        s.save()
        return HttpResponse('success')
    else:
        raise Http404

@csrf_exempt
def update_shop(request):
    pk = request.POST.get('pk', '')
    name = request.POST.get('name', '')
    owner = request.POST.get('owner', '')
    phone = request.POST.get('phone', '')
    address = request.POST.get('address', '')
    position = request.POST.get('position', '')
    desc = request.POST.get('desc', '')
    if pk and name:
        s = Shop.objects.get(pk=pk)
        s.name = name
        s.owner = owner
        s.phone = phone
        s.address = address
        s.position = position
        s.desc = desc
        s.save()
        return HttpResponse('success')
    else:
        raise Http404

@csrf_exempt
def disable_shop(request):
    pk = request.POST.get('pk', '')
    if pk:
        s = Shop.objects.get(pk=pk)
        if s:
            s.disable = True
            s.save()
            return HttpResponse('success')
        else:
            return HttpResponseNotFound('error')
    else:
        raise Http404

@csrf_exempt
def get_storages(request): #todo: batch
    all = Storage.objects.all()
    json = serializers.serialize('json', all)
    return HttpResponse(json)

@csrf_exempt
def get_inbounds(request): #todo: batch
    all = InBound.objects.all()
    json = serializers.serialize('json', all)
    return HttpResponse(json)

@csrf_exempt
def new_inbound(request):
    product = request.POST.get('product', '')
    number_str = request.POST.get('number', '')
    source = request.POST.get('source', '')
    user = 'todo'
    number = 0
    try:
        number = int(number_str)
    except:
        pass
    if product and number:
        p = Product.objects.get(pk=product)
        if p:
            inb = InBound(product=p, number=number, source=source, user=user)
            s = Storage.objects.get(pk=product)
            if s:
                s.number = s.number + number
            else:
                s = Storage(product=product, number=number)
            with transaction.atomic():
                inb.save()
                s.save()
            return HttpResponse('success')
        else:
            return HttpResponseNotFound('error')
    else:
        raise Http404


@csrf_exempt
def get_outbounds(request):
    pass


@csrf_exempt
def new_outbound(request):
    pass

@csrf_exempt
def update_outbound(request): #todo: compare ctime vs last time
    pass

@csrf_exempt
def close_outbound(request): #storage back
    pass

@csrf_exempt
def new_distribution(request):
    pass

