from django.shortcuts import render

# Create your views here.

from django.views.generic.base import View      #View视图
from django.http import HttpResponse,HttpResponseRedirect
from apps.users.form import LoginForm    #表单验证
from django.contrib.auth import authenticate,login,logout   #登录时的表单认证，退出登录
from django.urls import reverse       #重定向参数
from django.contrib.auth.mixins import LoginRequiredMixin       #判断登录状态

#django的登录显示及验证
class LoginView(View):
    #如果使用get,#点击按钮#,跳转到login.html
    def get(self,request,*args,**kwargs):
        #获取next
        next = request.GET.get('next','')
        return render(request,'login.html',{'next':next})

    #如果使用的是post，#表单提交#，那么
    def post(self,request,*args,**kwargs):
        '''
        用户登陆处理逻辑：
        (1).实例化form.py中的表单限制类，参数为(request.POST)
        (2).用户输入用户名和密码，首先进入django内置的合法限制类--form.py中的LoginForm类。
            不合法：默认会报出视图函数没有返回HttpResponse对象的异常,我们在制图函数中重写页面，
                   如果不合法，那么重新返回login.html页面，并携带不合法的数据。不再往下进行。
            合法，通过--- 对象.cleaned_data['username/password']进行获取用户输入的数据，往下将继续进行
        (3).django内置表单验证模块，用于验证用户名和密码的方法，有两个参数username和password
            验证成功返回验证对象(数据库中的对象),失败则是None
        (4).判断：
                如果返回的对象不为空：那么表示数据库中有该对象，那么
                                    通过django内置的表单登录方法login(request,返回的对象)，
                                    进行登录操作，并重定向到index页面
                如果为空：那么表示数据库中没有该对象，
                         直接返回login.html重新登陆，
                         并携带msg(用户名或密码错误)的提示信息，以及用户不正确的数据信息。
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        #实例化LoginForm
        login_form = LoginForm(request.POST)

        #如果login_form表单是合法的，则获取，不合法直接阻挡。
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            pass_word = login_form.cleaned_data['password']

            #django内置用于验证用户名和密码的方法，有两个参数username和password
            #验证成功返回验证对象(数据库中的对象),失败则是None
            user = authenticate(username=user_name,password=pass_word)
            if user is not None:
                #登录模块，接受request和成功验证返回的user对象
                login(request,user)

                #判断next
                next = request.GET.get('next','')
                if next:
                    #如果next存在，就重定向到next值的url
                    return HttpResponseRedirect(next)

                #返回重定向到index页面，然后到url中进行匹配
                return HttpResponseRedirect(reverse('index'))
            else:
                #如果没有查询到用户，那么要求重新登陆，仍然返回login页面
                return render(request,'login.html',{'msg':'用户名密码错误','login_form':login_form})
        else:
            return render(request,'login.html',{'login_form':login_form})

#退出登录
class LogoutView(View):
    def get(self,request,*args,**kwargs):
        #退出登录
        logout(request)
        #重定向到index页面
        return HttpResponseRedirect(reverse('index'))


#之前方法实现登录验证
def index1(request):
    return render(request,'index1.html')
from apps.users.models import UserProfile
def login1(request):
    '''
    表单验证;
    如果是通过get方法进行访问，那么直接返回login1.html.
    如果使用post方法，那么表示是表单提交：
    (1).获取用户输入的表单数据
    (2).首先从数据库中查找用户名为用户输入的用户名的queryset对象(假设注册时用户名唯一，不重复)
    (3).如果queryset对象存在，通过迭代取出对象中的密码，(由于用户名唯一，密码也一定唯一)
        判断用户输入的密码是否于取出的密码相等，
            如果相等：允许登录，重定向index1页面。
            不相等，返回login1.html，并且携带正确的username以及错误提示信息。
    (4).如果queryset对象不存在，那么返回login.html，并携带错误提示信息。

    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request,'login1.html')
    if request.method == 'POST':
        #获取表单数据
        username = request.POST.get('username')
        password = request.POST.get('password')

        #从数据库中获取用户名为用户输入用户名的queryset对象，(假设注册时用户名不能重复，唯一的)
        users = UserProfile.objects.filter(username=username)

        if users.exists():           #判断queryset对象中是否有数据

            passwordlist = []
            for user in users:
                passwordlist.append(user.password)       #通过迭代取出密码

            if password in passwordlist:         #判断密码是否一致
                    return HttpResponseRedirect(reverse('index1'))
            else:
                return render(request,'login1.html',{'msg':'密码错误','username':username})
        else:
            return render(request, 'login1.html', {'msg': '用户名不存在'})


#个人中心--个人资料
class UserInfoView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        return render(request,'usercenter-info.html',{

        })
