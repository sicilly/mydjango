from django.test import Client
from django.urls import reverse
from test_plus import TestCase

from mydjango.news.models import News


class NewsViewsTest(TestCase):

    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")

        self.client = Client()        # 浏览器
        self.other_client = Client()  # 另外一个浏览器

        self.client.login(username="user01", password="password")  # 登录
        self.other_client.login(username="user02", password="password")

        self.first_news = News.objects.create(
            user=self.user,
            content="第一条动态"
        )

        self.second_news = News.objects.create(
            user=self.user,
            content="第二条动态"
        )

        self.third_news = News.objects.create(
            user=self.other_user,
            content="第一条动态的评论",
            reply=True,
            parent=self.first_news
        )

    def test_news_list(self):
        """测试动态列表页功能"""
        response = self.client.get(reverse("news:list"))
        assert response.status_code == 200  # 状态码应为200
        # context是个字典，里面有news_list，每一条动态都在里面
        assert self.first_news in response.context["news_list"]
        assert self.second_news in response.context["news_list"]
        assert self.third_news not in response.context["news_list"]  # 评论不在news_list里面

    def test_delete_news(self):
        """删除动态"""
        initial_count = News.objects.count()
        # 客户端发送post请求删除第二条动态
        response = self.client.post(reverse("news:delete_news", kwargs={"pk": self.second_news.pk}))
        assert response.status_code == 302  # 成功删除-重定向的状态码302
        assert News.objects.count() == initial_count - 1

    def test_post_news(self):
        """发送动态"""
        initial_count = News.objects.count()
        response = self.client.post(reverse("news:post_news"),
                                    {'news_content': '我爱将狗！'},
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")  # 表示发送Ajax Request请求
        assert response.status_code == 200
        assert News.objects.count() == initial_count + 1

    def test_like_news(self):
        """点赞"""
        response = self.client.post(reverse("news:post_like"),
                                    {'newsId': self.first_news.pk},  # 让用户 user01 给 first_news 点赞
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest"
                                    )  # 表示发送Ajax Request请求
        assert response.status_code == 200
        assert self.first_news.likers_count() == 1  # 点赞后数量==1
        assert self.user in self.first_news.get_likers()  # user01在get_liker()获取的点赞用户中
        assert response.json()["likers_count"] == 1

    def test_get_children(self):
        """获取动态的评论"""
        response = self.client.get(reverse('news:get_replies'),
                                   {"newsId":self.first_news.pk},
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest"
                                   )
        assert response.status_code == 200
        assert response.json()["newsid"] == self.first_news.pk.__str__()  # 要转成字符串
        assert self.first_news.content in response.json()["replies_html"]
        assert "第一条动态" in response.json()["replies_html"]

    def test_post_reply(self):
        """测试提交回复"""
        response = self.client.post(reverse("news:post_reply"),
                                    {'newsid': self.second_news.pk,
                                     'replyContent': "回复第二条新闻"},  # 让用户 user01 给 second_news 回复
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest"
                                    )  # 表示发送Ajax Request请求
        assert response.status_code == 200
        assert response.json()["newsid"] == str(self.second_news.pk)  # 强转成字符串
        assert response.json()["replies_count"] == 1
