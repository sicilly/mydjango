from django.urls import path

from mydjango.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    # 传用户名作为参数到详情页 这里的username和模型中的字段无关，应该和views.py中的slug_url_kwarg一致
    path("<str:username>/", view=user_detail_view, name="detail"),
    # path("<int:pk>", view=user_detail_view, name="detail"),  # pk的写法
]
