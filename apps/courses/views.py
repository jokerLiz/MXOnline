from django.shortcuts import render

# Create your views here.
from django.views.generic import View   #视图类
from apps.courses.models import *     #模型类
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger     #分页
class CourseView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'courselist.html')
