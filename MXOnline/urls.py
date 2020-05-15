from django.contrib import admin
from django.urls import path

import xadmin

from apps.users import views
from django.views.generic import TemplateView
from apps.users.views import LoginView,LogoutView

from django.conf.urls import url,include          #导入url(正则表达式方式)
from django.views.static import serve   #负责静态文件处理
from MXOnline.settings import MEDIA_ROOT      #导入MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/',xadmin.site.urls),

    path('',TemplateView.as_view(template_name='index.html'),name = 'index'),

    #login的url，进入LoginView的view中，
    #设置name是为了通过名字进行匹配与{% url ‘login’%}相匹配，也方便以后的修改和维护
    path('login/',LoginView.as_view(),name = 'login'),
    #退出登录
    path('logout/',LogoutView.as_view(),name = 'logout'),

    path('index1/',views.index1,name = 'index1'),
    path('login1/',views.login1,name = 'login1'),

    #配置上传文件的访问  document_root:指定文件的给根路径
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),


    #课程courses相关路由
    url(r'^course/',include(('apps.courses.urls','courses'),namespace='course')),
    #授课机构organizations路由
    url(r'^org/',include(('apps.organizations.urls','organizations'),namespace='org')),
    #用户操作operayions线相关路由
    url(r'^op/',include(('apps.operations.urls','operations'),namespace='op'))
]
