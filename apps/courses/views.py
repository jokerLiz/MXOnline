from django.shortcuts import render

# Create your views here.
from django.views.generic import View   #视图类
from apps.courses.models import *     #模型类
from pure_pagination import Paginator, PageNotAnInteger     #分页

from apps.operations.models import UserFavorite       #用户收藏表
from django.contrib.auth.mixins import LoginRequiredMixin    #必须登录使用的类
#课程页
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

        #获取热门课程 前三个
        hot_courses = Course.objects.order_by('-click_nums')[:3]

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
            'hot_courses':hot_courses          #热门课程前三个
        })


#课程详情页
class CourseDetailView(View):
    def get(self, request,course_id,*args, **kwargs):
        '''
        课程详情信息的展示
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        #根据前台传过来的id到数据库中获取该课程的信息
        course = Course.objects.get(id=int(course_id))
        #当用户点击一次，就记录一次该课程的点击数
        course.click_nums+=1
        course.save()

        #获取收藏状态
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:         #如果用户通过验证
            #查询用户是否收藏了该课程或该机构
            #fav_type=1 证明课程收藏，如果查出来，说明已经收藏了这个课
            if UserFavorite.objects.filter(user=request.user,fav_id=course_id,fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=2):
                has_fav_org = True

        return render(request,'coursedetail.html',{
            'course':course,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org
        })


#课程章节页
class CourseLessonView(LoginRequiredMixin,View):
    login_url = '/login/'           #进入该视图类时，如果用户没有登陆，就跳转到login进行登录
    '''
    章节信息的展示
    '''
    def get(self,request,course_id,*args,**kwargs):
        #获取用户点击的是哪个课程
        course = Course.objects.get(id = course_id)
        return render(request,'coursevideo.html',{
            'course':course
        })