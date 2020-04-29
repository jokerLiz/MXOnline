import xadmin
from apps.courses.models import Course

#不用继承admin.ModelAdmin
class CourseAdmin:
    # 默认显示的字段
    list_display = ["id", "name", "desc", "learn_times", "degree"]
    #搜索字段，按照什么字段搜索
    search_fields = ['name']
    #过滤器，根据什么字段进行过滤
    list_filter = ["id", "name","degree"]
xadmin.site.register(Course,CourseAdmin)