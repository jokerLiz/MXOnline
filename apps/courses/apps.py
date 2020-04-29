from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = 'apps.courses'
    #在后台中显示相应信息，而不是对象
    verbose_name = '课程管理'
