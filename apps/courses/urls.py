from django.conf.urls import url
from apps.courses.views import CourseView

urlpatterns = [
    #公开课列表展示
    url(r'^list/',CourseView.as_view(),name = 'list')
    ]