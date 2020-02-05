from django.conf import settings
from django.db import models
from django.db.models import Count
from slugify import slugify
from mdeditor.fields import MDTextField
from taggit.managers import TaggableManager


class ArticleCategory(models.Model):
    """文章类型"""
    catname = models.CharField(max_length=50, verbose_name='类别名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.catname

    class Meta:
        verbose_name = '文章类别'
        verbose_name_plural = verbose_name


class ArticleQuerySet(models.query.QuerySet):  # 继承查询集父类
    """自定义QuerySet，提高模型类的可用性"""

    def get_published(self):
        """返回已发表的文章"""
        return self.filter(status="P").order_by('-created_at')

    def get_drafts(self):
        """返回草稿箱的文章"""
        return self.filter(status="D").order_by('-updated_at')

    def get_counted_tags(self):
        """统计所有已发布的文章中，每一个标签的数量(大于0的)"""
        tag_dict = {}
        query = self.filter(status='P').annotate(tagged=Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1
        return tag_dict.items()


class Article(models.Model):
    STATUS = (("D", "Draft"), ("P", "Published"))  # 在前端渲染出来是select控件
    status = models.CharField(max_length=1, choices=STATUS, default='D', verbose_name='文章状态')  # 默认存入草稿箱
    category = models.ForeignKey(ArticleCategory, verbose_name="文章类别", null=True,
                                 blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="articles",
                             on_delete=models.SET_NULL, verbose_name='文章作者')
    title = models.CharField(max_length=255, blank=False, null=False, unique=False, verbose_name='文章标题')
    cover = models.ImageField(upload_to='blogs/covers/%Y/%m/%d/', verbose_name='文章封面')
    abstract = models.TextField(null=True, blank=True, verbose_name='文章摘要', default='此文章还没有摘要')
    content = MDTextField(verbose_name="文章内容")
    slug = models.SlugField(max_length=255, null=True, blank=True, verbose_name='(URL)别名')
    tags = TaggableManager(help_text='多个标签使用英文逗号(,)隔开', verbose_name='文章标签')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    objects = ArticleQuerySet.as_manager()  # 将Article.objects替换成自定义的查询管理集

    def __str__(self):
        return self.title  # Admin中文章管理会显示title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    # 重写Model的save方法
    def save(self, *args, **kwargs):
        if not self.slug:
            # 根据作者和标题生成文章在url中的别名
            self.slug = slugify(self.title)  # title必须是唯一的
            # 根据作者的username和标题生成文章在URL中的别名，保证了url的可读性也要保证唯一性
            # self.slug = slugify(self.title + self.user.username + "-" + uuid.uuid4().__str__()[0:8])
        super(Article, self).save(*args, **kwargs)
