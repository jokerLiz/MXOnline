from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from apps.users.views import *

urlpatterns = [
    #个人资料
    url(r'^info/$',UserInfoView.as_view(),name='info'),
    #我的课程
    url(r'^mycourse/$',login_required(TemplateView.as_view(template_name='usercenter-mycourse.html'), login_url='/login/'),{"current_page": "mycourse"}, name='mycourse'),
]