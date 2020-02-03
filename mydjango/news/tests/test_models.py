from test_plus import TestCase

from mydjango.news.models import News


class NewsModelsTest(TestCase):
    def setUp(self):
        self.user1 = self.make_user(username="user1", password="123456")
        self.user2 = self.make_user(username="user2", password="123456")
        self.news1 = News.objects.create(user=self.user1, content="第一条新闻")
        self.news2 = News.objects.create(user=self.user1, content="第二条新闻")
        self.news3 = News.objects.create(user=self.user2, content="第一次回复第一条新闻", reply=True, parent=self.news1)

    def test__str__(self):
        self.assertEqual(self.news1.__str__(), "第一条新闻")

    def test_switch_like(self):
        """测试点赞和取消赞"""
        self.news1.switch_like(self.user2)      # user2给news1点赞
        assert self.news1.likers_count() == 1   # news1的点赞数量应该是1
        self.news1.switch_like(self.user1)      # user1给news1点赞
        assert self.news1.likers_count() == 2   # news1的点赞数量应该是2
        assert self.user1 in self.news1.get_likers()  # user1应该在news1的点赞列表里
        assert self.user2 in self.news1.get_likers()  # user2应该在news1的点赞列表里
        self.news1.switch_like(self.user1)                # user1取消对news1点赞
        assert self.user1 not in self.news1.get_likers()  # user1应该不在news1的点赞列表里
        assert self.news1.likers_count() == 1   # news1的点赞数量应该是1

    def test_reply_this(self):
        """测试新闻回复api"""
        initial_count = News.objects.count()                      # 初始的news数
        assert self.news1.replies_count() == 1                    # news1应该有1条回复
        self.news1.reply_this(self.user2, "第二次回复第一条新闻")  # 新增了一条回复
        assert News.objects.count() == initial_count + 1          # news数比初始值多1
        assert self.news1.replies_count() == 2                    # news1应该有2条回复
        assert self.news3 in self.news1.get_children()            # news3应该是news1的回复



