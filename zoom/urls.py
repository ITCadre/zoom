"""zoom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    url(r'^zoom/$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^zoom/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^zoom/logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^zoom/admin/', admin.site.urls),
    url(r'^zoom/auth/', views.login),
    url(r'^zoom/do/diagrams/(?P<pk>[0-9]+)$', views.do_diagrams),
    url(r'^zoom/assign_user_to_diagram/$', views.assign_user_to_diagram),
    url(r'^zoom/device/(?P<pk>[0-9]+)/applications/$', views.device_applications),
    url(r'^zoom/application/(?P<pk>[0-9]+)/$', views.get_application),


]
