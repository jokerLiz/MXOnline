from django.db import models
from apps.users.models import BaseModel

#城市信息
class City(BaseModel):               #继承BaseModel类
    name = models.CharField(verbose_name="城市名", max_length=20)
    desc = models.CharField(verbose_name="城市描述", max_length=300)
    class Meta:
        verbose_name = "城市信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#机构信息
class CourseOrg(BaseModel):
    name = models.CharField(verbose_name="机构名称", max_length=50)
    tag = models.CharField(verbose_name="机构标签", max_length=100,default='')
    category = models.CharField(verbose_name='机构类别',max_length=100,choices=(('pxjg','培训机构'),('gr','个人'),('gx','高校')))
    click_nums = models.IntegerField(verbose_name="点击数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏数", default=0)
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo", max_length=100)
    address = models.CharField(verbose_name='机构地址',max_length=200)
    study_nums = models.IntegerField(verbose_name="学习人数", default=0)
    courses_nums = models.IntegerField(verbose_name="课程数", default=0)
    is_authentication = models.BooleanField(default=False, verbose_name="是否认证")
    is_gold = models.BooleanField(default=False, verbose_name="是否金牌")
    #关联外键city，一个城市有多个机构
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所在城市")

    class Meta:
        verbose_name = "机构信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


from apps.users.models import UserProfile
#教师信息
class Teacher(BaseModel):
    #与UserProfile一对一关联，一个教师只有一个账号
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="用户")
    #与机构一对多关联，一所机构有多个教师
    courseorg= models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(verbose_name="教师名", max_length=50)
    year = models.IntegerField(verbose_name='工作年限',default=0)
    company = models.CharField(verbose_name='就职公司',max_length=100)
    position = models.CharField(verbose_name='公司职位',max_length=100)
    trait = models.CharField(verbose_name='教学特点',max_length=300)
    click_nums = models.IntegerField(verbose_name="点击数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏数", default=0)
    age = models.IntegerField(verbose_name='年龄',default=0)
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)

    class Meta:
        verbose_name = "教师信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
