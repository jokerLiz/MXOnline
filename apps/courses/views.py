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
        #查询数据库中的所有信息，按照时间从大到小排序
        all_courses = Course.objects.all().order_by('-add_time')
        #查询信息的个数
        course_nums = all_courses.count()

        # 分页部分
        # 获取page，如果没找到或者出错都置page为1
        try:
            pindex = request.GET.get('page', 1)
        except PageNotAnInteger:
            pindex = 1

        # 参数1：作用对象，参数2：单页显示数量，参数3：request
        p = Paginator(all_courses, per_page=6, request=request)

        courses = p.page(pindex)  # 获取pindex页的信息

        return render(request,'courselist.html',{
            'all_courses':courses,
            'course_nums':course_nums
        })
