from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View   #视图类

from apps.courses.models import Course
from apps.organizations.models import *     #模型类
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger     #分页

from apps.organizations.form import AddAskForm      #导入form表单验证类

from apps.operations.models import UserFavorite  # 用户收藏表

# 机构列表
class OrgView(View):
    def get(self,request,*args,**kwargs):
        '''
        展示授课机构的列表页
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        all_orgs = CourseOrg.objects.all()         #查询所有的机构信息
        all_citys = City.objects.all()       #查询所有的城市信息


        #机构排名。根据点击数
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        #金牌与认证


        #筛选选项--机构类别
        category = request.GET.get('ct','')    #获取前台接口数据
        if category:
            # 过滤类别为用户选择的数据
            all_orgs = all_orgs.filter(category=category)


        #对所在城市进行筛选
        city_id = request.GET.get('city','')          #获取前台用户点击的选项数据
        if city_id:                       #如果存在，
            if city_id.isdigit():          #如果该数据合法，
                 all_orgs = all_orgs.filter(city_id=city_id)         #过滤用户选择的数据


        #对课程机构进行排序
        sort = request.GET.get('sort','')
        if sort == 'students':
            # 根据学生进行排序，-号代表倒序,一定要拿变量接着。
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            #根据课程数进行排序
            all_orgs = all_orgs.order_by('-course_nums')


        #经过过滤后的机构总数
        org_nums = all_orgs.count()


        #分页部分
        #获取page，如果没找到或者出错都置page为1
        try:
            pindex = request.GET.get('page', 1)
        except PageNotAnInteger:
            pindex = 1

        #参数1：作用对象，参数2：单页显示数量，参数3：request
        p = Paginator(all_orgs, per_page=5,request=request)

        orgs = p.page(pindex)          #获取page页的信息


        return render(request, 'org-list.html', {
            'all_orgs':orgs,          #机构列表
            'org_nums':org_nums,      #机构个数
            'all_citys':all_citys,    #所有城市
            'category':category,      #机构类别，用于联动和高亮
            'city_id': city_id,       #所选的城市id
            'sort':sort,              #排序规则，用于高亮的显示
            'hot_orgs':hot_orgs       #热门机构列表，前三个
            })

#机构详情
#home
class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):

        current_page = 'home'          #高亮值判断

        org = CourseOrg.objects.get(id=int(org_id))        #构信息

        # 每进入该页面一次，点击书加一
        org.click_nums += 1
        org.save()

        #机构讲师
        teachers = org.teacher_set.all()[:2]
        teacher_list = []
        for teacher in teachers:
            teacher_list.append(teacher)

        #判断当前用户是否收藏了该机构
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav_org = True

        return render(request,'org-detail-homepage.html',{
            'current_page':current_page,       #判断css样式显示
            'org':org,           #机构信息
            'teacher_list':teacher_list,         #讲师信息
            'has_fav_org':has_fav_org       #机构收藏
        })
#机构详情--机构课程
class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'orgcourse'  # 高亮值判断

        org = CourseOrg.objects.get(id=int(org_id))        #查询用户点击的机构

        courses = org.course_set.all()        #查询该机构所有的课程

        course_list = []
        for course in courses:
            course_list.append(course)

        # 判断当前用户是否收藏了该机构
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav_org = True
        return render(request,'org-detail-course.html',{
            'current_page':current_page,
            'org':org,            #机构
            'course_list':course_list,     #机构课程列表
            'has_fav_org':has_fav_org,      #当前用户是否收藏
        })
#机构详情--介绍
class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'orgdesc'  # 高亮值判断
        org = CourseOrg.objects.get(id=int(org_id))

        # 判断当前用户是否收藏了该机构
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav_org = True

        return render(request,'org-detail-desc.html',{
            'current_page':current_page,
            'org':org,
            'has_fav_org':has_fav_org
        })
#机构详情--讲师
class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'orgteacher'  # 高亮值判断

        org = CourseOrg.objects.get(id=int(org_id))

        #讲师
        teachers = org.teacher_set.all()
        teacher_list =[]
        for teacher in teachers:
            teacher_list.append(teacher)

        # 判断当前用户是否收藏了该机构
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav_org = True

        return render(request, 'org-detail-teachers.html', {
            'current_page':current_page,
            'org': org,
            'has_fav_org': has_fav_org,
            'teacher_list':teacher_list
        })



#立即咨询函数
class AddAsk(View):
    '''
    处理用户咨询模块

    '''
    def post(self,request,*args,**kwargs):
        #实例化
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():      #判断合法
            userask_form.save(commit=True)    #提交到数据库中
            return JsonResponse({
                'status':'success',
                'msg':'提交成功'
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '添加出错'
            })

#讲师列表
class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()

        # 经过过滤后的机构总数
        teacher_nums = all_teachers.count()

        #人气排序
        sort = request.GET.get('sort','')
        if sort=='hot':
            all_teachers = all_teachers.order_by('-click_nums')     #根据点击数进行排序

        #讲师排行榜
        hot_teacher = Teacher.objects.all().order_by('-fav_nums')[:3]    #根据收藏数排序

        # 分页部分
        # 获取page，如果没找到或者出错都置page为1
        try:
            pindex = request.GET.get('page', 1)
        except PageNotAnInteger:
            pindex = 1

        # 参数1：作用对象，参数2：单页显示数量，参数3：request
        p = Paginator(all_teachers, per_page=3, request=request)

        teachers = p.page(pindex)  # 获取page页的信息

        return render(request,'teachers-list.html',{
            'all_teachers':teachers,       #讲师
            'teacher_nums':teacher_nums,      #讲师数量
            'sort':sort,             #获取的前端接口值
            'hot_teacher':hot_teacher    #讲师排行榜
        })

#讲师详情
class TeacherDetailView(View):
    def get(self, request,teacher_id, *args, **kwargs):

        teacher = Teacher.objects.get(id=int(teacher_id))   #获取用户点击的讲师信息

        #每进入讲师详情页面，该讲师的点击数就加一
        teacher.click_nums+=1
        teacher.save()

        #讲师收藏
        has_fav_Teacher = False
        has_fav_org = False
        if request.user.is_authenticated:         #如果用户通过验证
            #查询用户是否收藏了该课程或该机构
            #fav_type=1 证明课程收藏，如果查出来，说明已经收藏了这个课
            if UserFavorite.objects.filter(user=request.user,fav_id=int(teacher_id),fav_type=3):
                has_fav_Teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.org.id), fav_type=2):
                has_fav_org = True
        # print(has_fav_Teacher)

        #讲师排行
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        return render(request,'teacher-detail.html',{
            'teacher':teacher,             #讲师信息
            'has_fav_Teacher':has_fav_Teacher,       #用户是否收藏该讲师
            'has_fav_org':has_fav_org,
            'hot_teachers':hot_teachers       #讲师排行
        })



