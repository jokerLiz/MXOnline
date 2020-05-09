from django.shortcuts import render

# Create your views here.
from django.views.generic import View   #视图类
from apps.organizations.models import *     #模型类
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger     #分页
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
        # org_nums = all_orgs.count()          #查询机构的个数
        all_citys = City.objects.all()       #查询所有的城市信息

        #筛选选项--机构类别
        category = request.GET.get('ct','')    #获取前台接口数据
        if category:
            # 过滤类别为用户选择的数据
            all_orgs = all_orgs.filter(category=category)

        #对所在城市进行筛选
        city_id = request.GET.get('city','')          #获取前台用户点击的选项数据
        if city_id:             #如果存在，
            if city_id.isdigit():          #如果该数据合法，
                 all_orgs = all_orgs.filter(city_id=city_id)         #过滤用户选择的数据

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


        return render(request, 'orglist.html',{
            'all_orgs':orgs,
            'org_nums':org_nums,
            'all_citys':all_citys,
            'category':category,
            'city_id':city_id
            })