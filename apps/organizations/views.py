from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View   #视图类
from apps.organizations.models import *     #模型类
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger     #分页

from apps.organizations.form import AddAskForm      #导入form表单验证类

# 机构列表相关操作
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
            'sort':sort             #获取的前端接口值
        })

#讲师详情
class TeacherDetailView(View):
    def get(self, request,teacher_id, *args, **kwargs):

       teachers = Teacher.objects.get(id=int(teacher_id))   #获取用户点击的讲师信息

       return render(request,'teacher-detail.html',{
           'teachers':teachers
       })



