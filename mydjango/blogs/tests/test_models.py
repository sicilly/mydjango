from test_plus import TestCase

from mydjango.blogs.models import Article


class ArticlesModelsTest(TestCase):

    def setUp(self):
        """初始化操作"""
        self.user = self.make_user("test_user")  # make_user是创建测试用户
        self.other_user = self.make_user("other_test_user")
        self.article = Article.objects.create(
            title="第一篇文章",
            content="我爱将狗",
            status="P",
            user=self.user,
        )
        self.not_p_article = Article.objects.create(
            title="第二篇文章",
            content="我爱将狗我爱将狗我爱将狗我爱将狗我爱将狗",
            status="D",
            user=self.user,
        )

    def test_object_instance(self):
        """判断实例对象是否为Article类型"""
        assert isinstance(self.article, Article)
        assert isinstance(self.not_p_article, Article)
        assert isinstance(Article.objects.get_published()[0], Article)

    def test_return_values(self):
        """测试返回值"""
        assert self.article.status == "P"
        assert self.not_p_article.status == "D"
        assert self.article.__str__() == "第一篇文章"  # 因为__str__方法返回的是title.
        assert self.article in Article.objects.get_published()
        assert Article.objects.get_published()[0].title == "第一篇文章"
        assert self.not_p_article in Article.objects.get_drafts()

