from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager


class QuestionQuerySet(models.query.QuerySet):
    """自定义QuerySet，提高模型类的可用性"""

    def get_correct_answered(self):
        """已有正确答案的问题"""
        return self.filter(has_correct=True)

    def get_uncorrect_answered(self):
        """未被正确回答的问题"""
        return self.filter(has_correct=False)

    def get_counted_tags(self):
        """统计所有问题标签的数量(大于0的)"""
        tag_dict = {}
        for obj in self.all():
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1
        return tag_dict.items()


class Question(models.Model):
    STATUS = (("O", "Open"), ("C", "Close"), ("D", "Draft"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="questions",
                             on_delete=models.CASCADE, verbose_name='提问者')
    title = models.CharField(max_length=255, unique=False, verbose_name='问题标题')
    slug = models.SlugField(max_length=255, null=True, blank=True, verbose_name='(URL)别名')
    status = models.CharField(max_length=1, choices=STATUS, default='O', verbose_name='问题状态')
    content = models.TextField(verbose_name='问题内容')
    clicknum = models.IntegerField(verbose_name="浏览量", default=0)
    tags = TaggableManager(help_text='多个标签使用,(英文)隔开', verbose_name='问题标签')
    has_correct = models.BooleanField(default=False, verbose_name="是否有正确回答")  # 是否有接受的正确回答
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name
        ordering = ("-updated_at","-created_at",)

    def __str__(self):
        return self.title

    def get_all_answers(self):
        """获取所有的回答"""
        return Answer.objects.filter(question=self)  # self作为参数，当前的问题有多少个回答

    def count_answers(self):
        """回答的数量"""
        return self.get_all_answers().count()

    def get_accepted_answer(self):
        """被接受的回答"""
        return Answer.objects.get(question=self, is_accepted=True)


class Answer(models.Model):
    """问题答案"""
    # uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="answers",
                             on_delete=models.CASCADE, verbose_name='回答者')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", verbose_name='问题')
    content = models.TextField(verbose_name='答案内容')
    is_accepted = models.BooleanField(default=False, verbose_name='是否被接受')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # votes = GenericRelation(Vote, verbose_name='投票情况')  # 通过GenericRelation关联到Vote表

    class Meta:
        ordering = ('-is_accepted', '-created_at')  # 多字段排序
        verbose_name = '答案'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
