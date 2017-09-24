from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class User(models.Model):
#     name = models.CharField(max_length=128, primary_key=True)
#     psd = models.CharField(max_length=128)
#     level = models.PositiveSmallIntegerField(default=100)
#     disable = models.BooleanField(default=False)
#     creat_time = models.DateTimeField(auto_now_add=True)

class PermMeta(models.Model):
    'this is use for perm'
    class Meta:
        'global perms'
        permissions = (
            ("super", "this is god"),
            ("admin", "almost god"),
            ("car", "this is driver"),
        )

class Product(models.Model):
    name = models.CharField(max_length=128, primary_key=True)
    desc = models.CharField(max_length=512)
    disable = models.BooleanField(default=False)
    number = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)

class InBound(models.Model):
    product = models.ForeignKey(Product)
    number = models.PositiveIntegerField()
    source = models.CharField(max_length=128)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)

class Shop(models.Model):
    name = models.CharField(max_length=256)
    owner = models.CharField(max_length=128)
    phone = models.CharField(max_length=256) #{'home':123}
    address = models.CharField(max_length=512)
    position = models.CharField(max_length=256) #todo:x,y pos
    desc = models.CharField(max_length=256)
    disable = models.BooleanField(default=False)

class OutBound(models.Model):
    product = models.ForeignKey(Product)
    number = models.PositiveIntegerField()
    user = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    close = models.BooleanField(default=False)

class Distribution(models.Model):
    # todo: time time
    outbound = models.ForeignKey(OutBound)
    shop = models.ForeignKey(Shop)
    number = models.PositiveIntegerField()
    user = models.ForeignKey(User)
