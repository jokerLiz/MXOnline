from django.conf.urls import url,include
from apps.organizations.views import *

urlpatterns = [
#配置授课机构的列表展示
    url(r'^list/$',OrgView.as_view(),name = 'list'),

    #立即咨询
    url(r'^add_ask/$',AddAsk.as_view(),name = 'add_ask'),
    #讲师列表
    url(r'^teachers/$',TeacherListView.as_view(),name = 'teachers'),
    #讲师详情
    url(r'^teachers_detail/(?P<teacher_id>\d+)$',TeacherDetailView.as_view(),name = 'teachers_detail'),
]