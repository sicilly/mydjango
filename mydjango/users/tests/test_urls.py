# import pytest
# from django.urls import reverse, resolve
#
# from mydjango.users.models import User
#
# pytestmark = pytest.mark.django_db
#
#
# def test_detail(user: User):
#     assert (
#         reverse("users:detail", kwargs={"username": user.username})
#         == f"/users/{user.username}/"
#     )
#     assert resolve(f"/users/{user.username}/").view_name == "users:detail"
#
#
# def test_update():
#     assert reverse("users:update") == "/users/~update/"
#     assert resolve("/users/~update/").view_name == "users:update"
#
#
# def test_redirect():
#     assert reverse("users:redirect") == "/users/~redirect/"
#     assert resolve("/users/~redirect/").view_name == "users:redirect"
from django.urls import reverse, resolve
from test_plus import TestCase


class TestUserUrls(TestCase):
    def setUp(self):  # 创建用户
        self.user = self.make_user(username='testuser', password='password')

    # 详情页
    def test_detail_reverse(self):  # 反向解析测试 路由名称->路径字符串
        reversed_url = reverse("users:detail", kwargs={"username": self.user.username})
        self.assertEqual(reversed_url, f"/users/{self.user.username}/")

    def test_detail_resolve(self):  # 正向解析测试  路径字符串->路由名称
        resolved_urlname = resolve(f"/users/{self.user.username}/").view_name
        self.assertEqual(resolved_urlname, "users:detail")

    # 更新
    def test_update_reverse(self):  # 反向解析测试 路由名称->路径字符串
        reversed_url = reverse("users:update")
        self.assertEqual(reversed_url, "/users/~update/")

    def test_update_resolve(self):  # 正向解析测试  路径字符串->路由名称
        resolved_urlname = resolve("/users/~update/").view_name
        self.assertEqual(resolved_urlname, "users:update")

    # 重定向
    def test_redirect_reverse(self):  # 反向解析测试 路由名称->路径字符串
        reversed_url = reverse("users:redirect")
        self.assertEqual(reversed_url, "/users/~redirect/")

    def test_redirect_resolve(self):  # 正向解析测试  路径字符串->路由名称
        resolved_urlname = resolve("/users/~redirect/").view_name
        self.assertEqual(resolved_urlname, "users:redirect")
