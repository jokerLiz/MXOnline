from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View  # 视图类

from apps.operations.form import UserFavForm,CommentForm  # 表单验证类
from django.http import JsonResponse
from apps.operations.models import UserFavorite, CourseComments, Banner  # 用户收藏和用户评论模型类
from apps.courses.models import Course    #课程类
from apps.organizations.models import CourseOrg  #机构类
from apps.organizations.models import Teacher   #教师类

class AddFavView(View):
    '''
    用户收藏实现：
    前台使用ajax请求post方法，把该请求的数据存到数据库中,这相当于提交了一个表单
    1.当用户点击收藏按钮时，ajax请求提交，也就是进入该视图类了。
    2.首先判断用户是否登录，如果没有登陆，那么就跳转到login页面进行登录。
    3.如果用户登录了，那么就实例化表单验证，
      如果该表单对象是不合法的，那么就返回错误信息
      如果该表单对象是合法的，那么就会获取该表单中的fav_id和fav_type进一步操作。
    4,获取到以后到数据库中查询用户是否已经收藏了该数据，也就是在数据库中查询是否有这条收藏记录，
      如果有，那么就删除该条记录，(从已收藏到未收藏)
      如果没有，就插入该条记录。(未收藏到已收藏)

    '''
    # POST方法
    def post(self, request, *args, **kwargs):
        # 先判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登录'
            })
        # 实例化表单验证类
        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():  # 如果是合法的
            fav_id = user_fav_form.cleaned_data['fav_id']
            fav_type = user_fav_form.cleaned_data['fav_type']

            #判断用户是否已经收藏
            exist = UserFavorite.objects.filter(user=request.user,fav_id = fav_id,fav_type=fav_type)

            if exist:     #如果已经收藏，就删除该信息
                exist.delete()

                if fav_type ==1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums-=1
                    course.save()
                elif fav_type == 2:
                    courseorg = CourseOrg.objects.get(id=fav_id)
                    courseorg.fav_nums -= 1
                    courseorg.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums-=1
                    teacher.save()
                return JsonResponse({
                    'status':'success',
                    'msg':'收藏'
                })
            else:
                #添加数据，创建对象
                userfav = UserFavorite()
                userfav.user = request.user
                userfav.fav_id = fav_id
                userfav.fav_type = fav_type
                userfav.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': '已收藏'
                })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误'
            })

#发表评论
class CommentView(View):

    def post(self, request, *args, **kwargs):
        # 先判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登录'
            })
        #实例化表单
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comments = comment_form.cleaned_data['comments']
            course = comment_form.cleaned_data['course']

            ccmodel = CourseComments()
            ccmodel.comments = comments
            ccmodel.user = request.user
            ccmodel.course = course
            ccmodel.save()
            return JsonResponse({
                'status': 'success',
                'msg': '评论成功'
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '评论参数错误'
            })


#首页
class IndexView(View):
    def get(self, request, *args, **kwargs):
        '''
        首页展示
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        #轮播图，查询轮播图并按照index顺序排序
        banners = Banner.objects.all().order_by('index')

        #公开课，除去banner
        courses = Course.objects.filter(is_banner=False)[:7]

        # 小banner
        banner_courses = Course.objects.filter(is_banner=True)[:4]

        # 课程机构加载
        course_orgs = CourseOrg.objects.all()[:15]


        return render(request, 'index.html', {
            "banners": banners,         #轮播图
            "courses": courses,         #公开课
            'banner_courses':banner_courses,       #公开课中的轮播图
            "course_orgs": course_orgs,        #课程机构
        })