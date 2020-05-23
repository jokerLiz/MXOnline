from django.conf.urls import url
from apps.users.views import *

urlpatterns = [
    #个人资料
    url(r'^info/$',UserInfoView.as_view(),name='info')
]