from django.db import models
from apps.users.models import BaseModel
# Create your models here.
class City(BaseModel):
    城市名
    "描述")

    class CourseOrg(BaseModel):
        "机构名称"
        机构标签
        "

    "机构类别"
    "培训机构"), ("gr", "个人"), ("gx", "高校"))
    "点击数")
    收藏数
    ")
    image = models.ImageField(upload_to="org/%Y/%m", "logo", max_length=100)
    "机构地址"
    "学习人数")
    "课程数"

    "是否认证")
    "是否金牌")

    city = models.ForeignKey(City, on_delete=models.CASCADE, "所在城市")

    from apps.users.models import UserProfile


class Teacher(BaseModel):
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, "用户")
    "所属机构")
    u"教师名")
    , "工作年限")
    "就职公司")
    "公司职位")
    、, "教学特点")
    "点击数")
    "收藏数")
    "年龄")
    image = models.ImageField(upload_to="teacher/%Y/%m", "头像", max_length=100)

