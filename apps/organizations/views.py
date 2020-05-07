from django.shortcuts import render

# Create your views here.
from django.views.generic import View
class OrgView(View):
    def get(self,request,*args,**kwargs):
        '''
        展示授课机构的列表页
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        return render(request, 'orglist.html')