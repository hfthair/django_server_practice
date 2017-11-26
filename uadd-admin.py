from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Permission

name = 'admin'
psd ='admin'
i = 'admin'
u = User.objects.create_user(name, password=psd)
perm = get_object_or_404(Permission, codename=i)
u.user_permissions.add(perm)
u.save()

name = 'driver'
psd ='driver'
i = 'car'
u = User.objects.create_user(name, password=psd)
perm = get_object_or_404(Permission, codename=i)
u.user_permissions.add(perm)
u.save()

