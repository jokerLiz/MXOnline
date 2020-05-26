from django.conf.urls import url
from apps.operations.views import AddFavView, CommentView, DeleteFavView

urlpatterns = [
    #用户收藏
    url(r'^fav/$',AddFavView.as_view(),name='fav'),
    #用户评论
    url(r'^comment/$',CommentView.as_view(),name='comment'),
    # 删除收藏项
    url(r'^delete_fav/$', DeleteFavView.as_view(), name='delete_fav'),
]