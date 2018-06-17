import json
from django.core import serializers
from django.db import transaction
from django.http import (Http404, HttpResponse, HttpResponseForbidden,
                         HttpResponseNotFound, HttpResponseServerError)
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Permission

from japi.deco_perm import require_car_user, require_backend_user, \
        require_backend_user, authenticate_user
from japi.models import *


# Create your views here.
@csrf_exempt
def index(request):
    return HttpResponse('hello')

@csrf_exempt
def latest_version(request):
    info = {
        'version': 1.0,
        'url': '',
        'safe': True
    }
    json_response = json.dumps(info)
    return HttpResponse(json_response)

@csrf_exempt
def test_user(request):
    x = authenticate_user(request)
    if x and x.is_active:
        info = {
            'username': x.username,
            'perm': list(
                [i.replace('japi.', '') for i in x.get_all_permissions()]
                )
        }
        json_response = json.dumps(info)
        return HttpResponse(json_response)
    return HttpResponse('authorizated deny', status=401)

@require_backend_user
@csrf_exempt
def get_users(request):  # todo: batch
    objs = User.objects.all()
    dall = map(lambda x: {'pk': x.pk,
                          'fields': {'username': x.username,
                                     'is_active': x.is_active,
                                     'perm': list(x.get_all_permissions())
                                     }
                          },
               objs)
    dall = list(dall)
    json_response = json.dumps(dall)
    return HttpResponse(json_response)

@require_backend_user
@csrf_exempt
def add_user(request):
    name = request.POST.get('username', '')
    psd = request.POST.get('password', '')
    perms = request.POST.get('perms', '')
    perms = perms.split(':')
    if name and psd and perms:
        u = None
        try:
            u = User.objects.create_user(name, password=psd)
        except:
            raise Http404
        if u:
            for i in perms:
                try:
                    perm = get_object_or_404(Permission, codename=i)
                    u.user_permissions.add(perm)
                except:
                    pass
            return HttpResponse('success')
    raise Http404

@require_backend_user
@csrf_exempt
def change_user(request):
    name = request.POST.get('username', '')
    psd = request.POST.get('password', '')
    perms = request.POST.get('perms', '')
    perms = perms.split(':')
    if name:
        u = get_object_or_404(User, username=name)
        if psd:
            u.set_password(psd)
        if perms:
            u.user_permissions.clear()
            for i in perms:
                perm = get_object_or_404(Permission, codename=i)
                u.user_permissions.add(perm)
        return HttpResponse('success')
    raise Http404

@require_backend_user
@csrf_exempt
def disable_user(request):
    name = request.POST.get('username', '')
    if name:
        u = get_object_or_404(User, username=name)
        u.is_active = False
        return HttpResponse('success')
    raise Http404

@require_car_user
@csrf_exempt
def get_products(request):  # todo: batch
    objs = Product.objects.all()
    json_response = serializers.serialize('json', objs, use_natural_foreign_keys=True)
    return HttpResponse(json_response)

@require_backend_user
@csrf_exempt
def add_product(request):
    name = request.POST.get('name', '')
    desc = request.POST.get('desc', '')
    if name:
        p = Product(name=name, desc=desc)
        p.save()
        return HttpResponse('success')
    raise Http404

@require_backend_user
@csrf_exempt
def update_product(request):
    pk = request.POST.get('pk', '')
    name = request.POST.get('name', '')
    desc = request.POST.get('desc', '')
    if pk and name:
        p = get_object_or_404(Product, pk=pk)
        p.name = name
        p.desc = desc
        p.save()
        return HttpResponse('success')
    raise Http404

@require_backend_user
@csrf_exempt
def disable_product(request):
    pk = request.POST.get('pk', '')
    if pk:
        p = get_object_or_404(Product, pk=pk)
        p.disable = True
        p.save()
        return HttpResponse('success')
    raise Http404

@require_car_user
@csrf_exempt
def get_shops(request):  # todo: batch
    objs = Shop.objects.all()
    json_response = serializers.serialize('json', objs, use_natural_foreign_keys=True)
    return HttpResponse(json_response)

@require_backend_user
@csrf_exempt
def add_shop(request):
    name = request.POST.get('name', '')
    owner = request.POST.get('owner', '')
    phone = request.POST.get('phone', '')
    address = request.POST.get('address', '')
    position = request.POST.get('position', '')
    desc = request.POST.get('desc', '')
    if name:
        s = Shop(name=name, owner=owner, phone=phone,
                 address=address, position=position, desc=desc)
        s.save()
        return HttpResponse('success')
    else:
        raise Http404

@require_backend_user
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
        s = get_object_or_404(Shop, pk=pk)
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

@require_backend_user
@csrf_exempt
def disable_shop(request):
    pk = request.POST.get('pk', '')
    if pk:
        s = get_object_or_404(Shop, pk=pk)
        s.disable = True
        s.save()
        return HttpResponse('success')
    raise Http404

@require_car_user
@csrf_exempt
def get_inbounds(request):  # todo: batch
    objs = InBound.objects.all()
    json_response = serializers.serialize('json', objs, use_natural_foreign_keys=True)
    return HttpResponse(json_response)

@require_car_user
@csrf_exempt
def new_inbound(request):
    product = request.POST.get('product', '')
    number_str = request.POST.get('number', '')
    source = request.POST.get('source', '')
    user = request.user
    number = 0
    try:
        number = int(number_str)
    except:
        pass
    if product and number:
        p = get_object_or_404(Product, pk=product)
        inb = InBound(product=p, number=number, source=source, user=user)
        p.number = p.number + number
        with transaction.atomic():
            inb.save()
            p.save()
            return HttpResponse('success')
    raise Http404

@require_car_user
@csrf_exempt
def get_outbounds(request):  # todo: batch
    objs = OutBound.objects.all().order_by('-last_update')
    json_response = serializers.serialize('json', objs, use_natural_foreign_keys=True)
    return HttpResponse(json_response)

@require_car_user
@csrf_exempt
def get_outbound_detail(request):
    obj = None
    pk = request.GET.get('pk', '')
    if pk:
        obj = OutBound.objects.get(pk=pk)
    else:
        objs = OutBound.objects.filter(user=request.user)
        if objs:
            obj = objs[0]
    if obj:
        dises = Distribution.objects.filter(outbound=obj)
        tmp = [obj]
        if dises:
            tmp.extend(dises)
        json_response = serializers.serialize('json', tmp, use_natural_foreign_keys=True)
        return HttpResponse(json_response)
    raise Http404

@require_car_user
@csrf_exempt
def new_outbound(request):
    product = request.POST.get('product', '')
    number_str = request.POST.get('number', '')
    user = request.user
    number = 0
    try:
        number = int(number_str)
    except:
        pass
    if product and number:
        p = get_object_or_404(Product, pk=product)
        outb = OutBound(product=p, number=number, user=user)
        if p.number >= number:
            p.number = p.number - number
            with transaction.atomic():
                outb.save()
                p.save()
                return HttpResponse('success')
    raise Http404

@require_car_user
@csrf_exempt
def update_outbound(request):  # todo: compare ctime vs last time
    raise Http404

@require_car_user
@csrf_exempt
def close_outbound(request):  # storage back
    pk = request.POST.get('pk', '')
    if pk:
        outb = get_object_or_404(OutBound, pk=pk)
        if outb.number > 0:
            if outb.product:
                p = outb.product
                if p:
                    p.number = p.number + outb.number
                    outb.close = True
                    with transaction.atomic():
                        p.save()
                        outb.save()
                        return HttpResponse('success')
        else:
            outb.close = True
            outb.save()
            return HttpResponse('success')
    raise Http404

@require_car_user
@csrf_exempt
def new_distribution(request):
    pk = request.POST.get('pk', '')
    pk_shop = request.POST.get('shop', '')
    number_str = request.POST.get('number', '')
    number = 0
    try:
        number = int(number_str)
    except:
        pass
    if pk and pk_shop and number:
        outb = get_object_or_404(OutBound, pk=pk)
        shop = get_object_or_404(Shop, pk=pk_shop)
        if outb.number >= number:
            dis = Distribution(outbound=outb, shop=shop, number=number, user=request.user)
            outb.number = outb.number - number
            with transaction.atomic():
                dis.save()
                outb.save()
                return HttpResponse('success')
    raise Http404
