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

        #取出筛选选项,根据课程标签(category)进行筛选
        cate_list = []
        for course in all_courses:
            if course.category not in cate_list:
                cate_list.append(course.category)

        #根据筛选选项筛选课程数据
        cate_name = request.GET.get('ct','')   # 获取前台接口数据
        if cate_name:
            # 过滤类别为用户选择的数据
            all_courses = all_courses.filter(category=cate_name)


        #排序
        sort = request.GET.get('sort','')
        if sort == 'hot':
            # 根据学生进行排序，-号代表倒序,一定要拿变量接着。
            all_courses = all_courses.order_by('-click_nums')
        elif sort == 'students':
            # 根据课程数进行排序
            all_courses = all_courses.order_by('-students')

        #查询课程数据的个数
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
            'all_courses':courses,             #课程信息
            'course_nums':course_nums,         #课程数量
            'cate_list':cate_list,             #筛选选项列表
            'cate_name':cate_name,             #点击的选项名，用于前端的高亮和联动
            'sort':sort,                       #点击的排序规则，用于前端的高亮变换
        })
