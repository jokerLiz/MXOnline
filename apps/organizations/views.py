from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from apps.organizations.models import *
class OrgView(View):
    def get(self,request,*args,**kwargs):
        '''
        展示授课机构的列表页
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        #查询所有的机构信息
        all_orgs = CourseOrg.objects.all()

        #查询机构的个数
        org_nums = all_orgs.count()

        #查询所有的城市信息
        all_citys = City.objects.all()


        return render(request, 'orglist.html',{
            'all_orgs':all_orgs,
            'org_nums':org_nums,
            'all_citys':all_citys
            })