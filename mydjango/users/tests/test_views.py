# import pytest
# from django.test import RequestFactory
#
# from mydjango.users.models import User
# from mydjango.users.views import UserRedirectView, UserUpdateView
#
# pytestmark = pytest.mark.django_db
#
#
# class TestUserUpdateView:
#     """
#     TODO:
#         extracting view initialization code as class-scoped fixture
#         would be great if only pytest-django supported non-function-scoped
#         fixture db access -- this is a work-in-progress for now:
#         https://github.com/pytest-dev/pytest-django/pull/258
#     """
#
#     def test_get_success_url(self, user: User, request_factory: RequestFactory):
#         view = UserUpdateView()
#         request = request_factory.get("/fake-url/")
#         request.user = user
#
#         view.request = request
#
#         assert view.get_success_url() == f"/users/{user.username}/"
#
#     def test_get_object(self, user: User, request_factory: RequestFactory):
#         view = UserUpdateView()
#         request = request_factory.get("/fake-url/")
#         request.user = user
#
#         view.request = request
#
#         assert view.get_object() == user
#
#
# class TestUserRedirectView:
#     def test_get_redirect_url(self, user: User, request_factory: RequestFactory):
#         view = UserRedirectView()
#         request = request_factory.get("/fake-url")
#         request.user = user
#
#         view.request = request
#
#         assert view.get_redirect_url() == f"/users/{user.username}/"

from django.test import RequestFactory
from test_plus import TestCase

from mydjango.users.views import UserUpdateView, UserRedirectView


# 公共父类
class BaseUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()  # 产生实例
        self.user = self.make_user(username='testuser', password='password')  # 产生测试用户


class TestUserUpdateView(BaseUserTestCase):

    def setUp(self):
        super(TestUserUpdateView, self).setUp()
        self.view = UserUpdateView()  # 调用构造函数产生视图
        request = self.factory.get('/fake-url')  # 发起一个get请求
        request.user = self.user  # 要登录
        self.view.request = request

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(), f"/users/{self.user.username}/")

    def test_get_object(self):
        self.assertEqual(self.view.get_object(), self.user)


class TestUserRedirectView(BaseUserTestCase):

    def setUp(self):
        super(TestUserRedirectView, self).setUp()
        self.view = UserRedirectView()
        request = self.factory.get('/fake-url')
        request.user = self.user
        self.view.request = request

    def test_get_redirect_url(self):
        self.assertEqual(self.view.get_redirect_url(), f"/users/{self.user.username}/")
