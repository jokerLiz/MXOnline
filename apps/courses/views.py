from django.shortcuts import render

# Create your views here.
from django.views.generic import View   #视图类
from apps.courses.models import *     #模型类
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger     #分页
class CourseView(View):
    def get(self, request, *args, **kwargs):
        '''
        公开课，课程的展示
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        all_courses = Course.objects.all()
        course_nums = all_courses.count()

        return render(request,'courselist.html',{
            'all_courses':all_courses,
            'course_nums':course_nums
        })
