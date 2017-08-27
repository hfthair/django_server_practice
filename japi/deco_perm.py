import base64
from functools import wraps
from django.contrib.auth import authenticate
from django.http import HttpResponse

def __authenticate_user(request):
    au = request.META.get('HTTP_AUTHORIZATION')
    if au:
        up = base64.b64decode(au)
        up = up.decode('utf8')
        if ':' in up:
            u, p = up.split(':', 1)
            user = authenticate(username=u, password=p)
            return user

def __require_user_perm(func_view, perms):
    @wraps(func_view)
    def decorator(request, *args, **kwargs):
        user = __authenticate_user(request)
        if user and user.is_active:
            for perm in perms:
                if user.has_perm(perm):
                    request.user = user
                    return func_view(request, *args, **kwargs)
            return HttpResponse('permission deny', status=403)
        return HttpResponse('authorizated deny', status=401)
    return decorator

def require_super_user(func_view):
    return __require_user_perm(func_view, ['japi.super'])

def require_backend_user(func_view):
    return __require_user_perm(func_view, ['japi.super', 'japi.admin'])

def require_car_user(func_view):
    return __require_user_perm(func_view, ['japi.super', 'japi.admin', 'japi.car'])
            
        