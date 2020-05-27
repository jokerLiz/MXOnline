from django.conf.urls import url,include
from apps.organizations.views import *

urlpatterns = [
    #配置授课机构的列表展示
    url(r'^list/$',OrgView.as_view(),name = 'list'),

    #机构详情页
    #home
    url(r'^home/(?P<org_id>\d+)$',OrgHomeView.as_view(),name = 'home'),
    #机构课程
    url(r'^orgcourse/(?P<org_id>\d+)$',OrgCourseView.as_view(),name = 'orgcourse'),
    #机构介绍
    url(r'^orgdesc/(?P<org_id>\d+)$',OrgDescView.as_view(),name = 'orgdesc'),
    #机构讲师
    url(r'^orgteacher/(?P<org_id>\d+)$',OrgTeacherView.as_view(),name = 'orgteacher'),


    #立即咨询
    url(r'^add_ask/$',AddAsk.as_view(),name = 'add_ask'),


    #讲师列表
    url(r'^teachers/$',TeacherListView.as_view(),name = 'teachers'),
    #讲师详情
    url(r'^teachers_detail/(?P<teacher_id>\d+)$',TeacherDetailView.as_view(),name = 'teachers_detail'),

]