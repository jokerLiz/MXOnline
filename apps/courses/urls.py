from django.conf.urls import url
from apps.courses.views import CourseView,CourseDetailView,CourseLessonView



urlpatterns = [
    #公开课列表展示
    url(r'^list/$',CourseView.as_view(),name = 'list'),

    #课程详情页
    url(r'^(?P<course_id>\d+)/$',CourseDetailView.as_view(),name = 'detail'),

    #章节信息
    url(r'^(?P<course_id>\d+)/lesson/$',CourseLessonView.as_view(),name='lesson')
    ]