from django.shortcuts import render

# Create your views here.
from django.views.generic import View   #视图类
from apps.courses.models import *     #模型类
from pure_pagination import Paginator, PageNotAnInteger     #分页

from apps.operations.models import UserFavorite, UserCourse, CourseComments  # 用户收藏表,用户课程表
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

        return render(request, 'course-list.html', {
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

        #相关课程推荐
        #根据课程标签进行推荐
        course_tag = course.tag        #获取当前课程的标签
        course_list = []     #用于存储课程的列表
        if course_tag:
            # 过滤课程标签在该标签中的课程，并去除id为当前课程的项,取前三个，  返回若干个queryset对象
            course_list = Course.objects.filter(tag__contains=course.tag).exclude(id=course.id)[:3]
        # print(course_list)


        #根据CourseTag类完成课程推荐
        

        return render(request, 'course-detail.html', {
            'course':course,        #用户点击的课程信息
            'has_fav_course':has_fav_course,     #用户是否收藏该课程
            'has_fav_org':has_fav_org,          #用户是否收藏该课程对应的机构
            'course_list':course_list         #课程推荐项
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

        # 如果用户点击学习了该课程，那么就添加到 用户课程 的表中
        #判断用户之前是否学习过该课程。
        if not UserCourse.objects.filter(user=request.user,course=course):    #单例模式
            uscour = UserCourse()  # 实例化表
            uscour.user = request.user   #增加用户课程表
            uscour.course = course
            uscour.save()

        #学过该课的同学该学过模块
        all_user = UserCourse.objects.filter(course=course)    #查询学过该课的用户都有谁
        user_ids = [users.user_id for users in all_user]     #循环遍历这些用户，添加到数组中
        # print(user_ids)
        # 筛选出表中user_id在数组中的queryset对象
        course_all = UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')
        course_list = []         #用于存储课程列表
        for icourse in course_all:         #遍历queryset对象
            if icourse.course_id != int(course_id) and icourse.course not in course_list:
                #如果数组中遍历到当前课程，就pass掉,   如果该课程对象没有在列表中，就加入该列表
                course_list.append(icourse.course)
        course_list = course_list[:5]
        # print(course_id)
        # print(course.id)
        # print(course_list)


        #查询该课程的资源
        courseresource = CourseResource.objects.filter(course=course)


        return render(request, 'course-video.html', {
            'course':course,        #用户学习的课程
            'courseresource':courseresource,           #该课程的资源
            'course_list':course_list      #学过该课程的还学过的课程
        })


#评论模块
class CourseCommentView(LoginRequiredMixin,View):
    login_url = '/login/'  # 进入该视图类时，如果用户没有登陆，就跳转到login进行登录
    '''
    评论信息的展示，由于和video在一个页面中，要使用同一组数据，所以要进行
    '''

    def get(self, request, course_id, *args, **kwargs):
        # 获取用户点击的是哪个课程
        course = Course.objects.get(id=course_id)

        # 如果用户点击学习了该课程，那么就添加到 用户课程 的表中
        # 判断用户之前是否学习过该课程。
        if not UserCourse.objects.filter(user=request.user, course=course):  # 单例模式
            uscour = UserCourse()  # 实例化表
            uscour.user = request.user  # 增加用户课程表
            uscour.course = course
            uscour.save()

        # 学过该课的同学该学过模块
        all_user = UserCourse.objects.filter(course=course)  # 查询学过该课的用户都有谁
        user_ids = [users.user_id for users in all_user]  # 循环遍历这些用户，添加到数组中
        # print(user_ids)
        # 筛选出表中user_id在数组中的queryset对象
        course_all = UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')
        course_list = []  # 用于存储课程列表
        for icourse in course_all:  # 遍历queryset对象
            if icourse.course_id != int(course_id) and icourse.course not in course_list:
                # 如果数组中遍历到当前课程，就pass掉,   如果该课程对象没有在列表中，就加入该列表
                course_list.append(icourse.course)
        course_list = course_list[:5]
        # print(course_id)
        # print(course.id)
        # print(course_list)

        # 查询该课程的资源
        courseresource = CourseResource.objects.filter(course=course)

        #加载数据库中评论
        comments = CourseComments.objects.filter(course=course)      #查询有关该课的评论


        return render(request, 'course-comment.html', {
            'course': course,  # 用户学习的课程
            'courseresource': courseresource,  # 该课程的资源
            'course_list': course_list,  # 学过该课程的还学过的课程
            'comments':comments       #该课的用户评论
        })