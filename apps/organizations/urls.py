from django.conf.urls import url,include
from apps.organizations.views import *
urlpatterns = [
#配置授课机构的列表展示
    url(r'^list/$',OrgView.as_view(),name = 'list'),
    url(r'^add_ask/$',AddAsk.as_view(),name = 'add_ask'),
]