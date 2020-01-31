# import pytest
#
# from mydjango.users.models import User
#
# pytestmark = pytest.mark.django_db
#
#
# def test_user_get_absolute_url(user: User):
#     assert user.get_absolute_url() == f"/users/{user.username}/"

from test_plus import TestCase


# 测试自定义用户模型类
class TestUser(TestCase):
    def setUp(self):
        self.user = self.make_user(username='testuser', password='password')

    def test__str__(self):
        self.assertEqual(self.user.__str__(), 'testuser')

    def test_get_profile_name(self):
        assert self.user.get_profile_name() == 'testuser'
        self.user.nickname = '昵称'
        assert self.user.get_profile_name() == '昵称'

    def test_get_absolute_url(self):
        # assert self.user.get_absolute_url() == f"/users/{self.user.username}/"
        self.assertEqual(self.user.get_absolute_url(), f"/users/{self.user.username}/")
