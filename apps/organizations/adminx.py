from apps.organizations.models import *

import xadmin

class CityAdmin:
    pass
xadmin.site.register(City,CityAdmin)

class CourseOrgAdmin:
    pass
xadmin.site.register(CourseOrg,CourseOrgAdmin)

class TeacherAdmin:
    list_display = ["id", "name",'courseorg']
xadmin.site.register(Teacher,TeacherAdmin)