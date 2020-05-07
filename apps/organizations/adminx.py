import xadmin

from apps.organizations.models import Teacher, CourseOrg, City

class CityAdmin(object):
    list_display = ["id", "name", "desc"]
    search_fields = ["name", "desc"]
    list_filter = ["name", "desc", "add_time"]
    list_editable = ["name", "desc"]

class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']
    style_fields = {
        "desc": "ueditor"
    }
class TeacherAdmin(object):
    #默认显示字段
    list_display = ['org', 'name', 'work_years', 'work_company']
    #搜索字段
    search_fields = ['org', 'name', 'work_years', 'work_company']
    #过滤器
    list_filter = ['org', 'name', 'work_years', 'work_company']


#注册模型类
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)