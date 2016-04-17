"""codeccnitscom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from main.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Home.as_view(), name='HomePage'),
    url(r'^sample/$', Sample.as_view(), name='Sample'),
    url(r'^save_code/$', SaveCode.as_view(), name='SaveCode'),
    url(r'^(?P<slug>[\w\-]+)$', ViewCode.as_view(), name='ViewCode'),
    url(r'^(?P<slug>[\w\-]+)/$', ViewCode.as_view(), name='ViewCodeFull'),
    url(r'^compile/$', CompileCode.as_view(), name='CompileCode'),
    url(r'^run/$', CompileCode.as_view(), name='RunCode'),
]
