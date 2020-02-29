from django.urls import path

from mydjango.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    user_articles_detail_view
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),  # 重定向
    path("~update/", view=user_update_view, name="update"),  # 更新
    # 传用户名作为参数到详情页 这里的username和模型中的字段无关，应该和views.py中的slug_url_kwarg一致
    path("<str:username>/", view=user_detail_view, name="detail"),                  # 用户详情
    path("<str:username>/articles/", view=user_articles_detail_view, name="user_articles"),  # 用户发表的文章
    # path("<int:pk>", view=user_detail_view, name="detail"),  # pk的写法
]
