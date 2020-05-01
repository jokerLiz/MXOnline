from django.contrib import admin
from django.urls import path

import xadmin
from apps.users import views
from django.views.generic import TemplateView
from apps.users.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/',xadmin.site.urls),

    # path('',views.index),
    path('',TemplateView.as_view(template_name='index.html'),name = 'index'),

    # path('login/',views.login,name = 'login')

    #login的url，进入LoginView的view中，
    #设置name是为了通过名字进行匹配与{% url ‘login’%}相匹配，也方便以后的修改和维护
    path('login/',LoginView.as_view(),name = 'login')
]
