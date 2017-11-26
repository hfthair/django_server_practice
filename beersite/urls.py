"""beersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from japi import views as japi

urlpatterns = [
    url(r'^api/user/get/', japi.get_users),
    url(r'^api/user/add/', japi.add_user),
    url(r'^api/user/test/', japi.test_user),
    url(r'^api/user/change/', japi.change_user),
    url(r'^api/user/disable/', japi.disable_user),
    url(r'^api/inbound/get/', japi.get_inbounds),
    url(r'^api/inbound/add/', japi.new_inbound),
    url(r'^api/outbound/get/', japi.get_outbounds),
    url(r'^api/outbound/add/', japi.new_outbound),
    url(r'^api/outbound/close/', japi.close_outbound),
    url(r'^api/outbound/detail/', japi.get_outbound_detail),
    url(r'^api/outbound/distribut/', japi.new_distribution),
    url(r'^api/product/get/', japi.get_products),
    url(r'^api/product/add/', japi.add_product),
    url(r'^api/product/update/', japi.update_product),
    url(r'^api/product/remove/', japi.disable_product),
    url(r'^api/shop/get/', japi.get_shops),
    url(r'^api/shop/add/', japi.add_shop),
    url(r'^api/shop/update/', japi.update_shop),
    url(r'^api/shop/remove/', japi.disable_shop),
    url(r'^api/version/latest/', japi.latest_version),
    url(r'^api/', japi.index),
    url(r'^admin/', admin.site.urls),
]
