from django import forms     #导入forms表单验证

from apps.operations.models import UserFavorite,CourseComments   #导入要存储的数据库

#用户收藏存储
class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite       #指定数据库
        fields = ['fav_id','fav_type']         #筛选要存的字段


#评论表单限制
class CommentForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ['course','comments']

