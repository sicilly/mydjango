import uuid
from collections import Counter
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from slugify import slugify
from taggit.managers import TaggableManager

from mydjango.notifications.views import notification_handler


class Vote(models.Model):
    """使用Django中的ContentType, 同时关联用户对问题和回答的投票"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes',
                             on_delete=models.CASCADE, verbose_name='用户')
    value = models.BooleanField(default=True, verbose_name='赞同或反对')  # True赞同，False反对
    # GenericForeignKey设置
    content_type = models.ForeignKey(ContentType, related_name='votes_on', on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)  # 关联到整形和非整形的逐渐上，用CharField
    vote = GenericForeignKey('content_type', 'object_id')  # 等同于GenericForeignKey()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '投票'
        verbose_name_plural = verbose_name


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
        return tag_dict.items()  # 返回的是键值对

    def get_questions_by_user(self, user):
        """获取指定用户的所有问题"""
        return self.filter(user=user).order_by('-updated_at')


class Question(models.Model):
    STATUS = (("O", "Open"), ("C", "Close"), ("D", "Draft"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="questions",
                             on_delete=models.CASCADE, verbose_name='提问者')
    title = models.CharField(max_length=255, unique=False, verbose_name='问题标题')
    slug = models.SlugField(max_length=255, null=True, blank=True, verbose_name='(URL)别名')
    status = models.CharField(max_length=1, choices=STATUS, default='O', verbose_name='问题状态')
    content = MarkdownxField(verbose_name='问题内容')
    clicknum = models.IntegerField(verbose_name="浏览量", default=0)
    tags = TaggableManager(help_text='多个标签使用,(英文)隔开', verbose_name='问题标签')
    has_correct = models.BooleanField(default=False, verbose_name="是否有正确回答")  # 是否有接受的正确回答
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    votes = GenericRelation(Vote, verbose_name='投票情况')  # 通过GenericRelation关联到Vote表，不是实际的字段
    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name
        ordering = ("-updated_at","-created_at",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # 现在允许slug重复
        super(Question, self).save(*args, **kwargs)

    def get_markdown(self):
        return markdownify(self.content)

    def get_all_answers(self):
        """获取所有的回答"""
        return Answer.objects.filter(question=self)  # self作为参数，当前的问题有多少个回答

    def count_answers(self):
        """回答的数量"""
        return self.get_all_answers().count()

    def get_accepted_answer(self):
        """被接受的回答"""
        return Answer.objects.get(question=self, is_accepted=True)

    def get_upvoters(self):
        """赞同的用户"""
        return [vote.user for vote in self.votes.filter(value=True)]

    def get_downvoters(self):
        """反对的用户"""
        return [vote.user for vote in self.votes.filter(value=False)]

    def total_votes(self):
        # """得票数: 赞成票-反对票"""
        # return len(self.get_upvoters())-len(self.get_downvoters())
        dic = Counter(self.votes.values_list('value', flat=True))  # Counter赞同票多少，反对票少数
        return dic[True] - dic[False]


class Answer(models.Model):
    """问题答案"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="answers",on_delete=models.CASCADE, verbose_name='回答者')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", verbose_name='问题')
    content = MarkdownxField(verbose_name='答案内容')
    is_accepted = models.BooleanField(default=False, verbose_name='是否被接受')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    votes = GenericRelation(Vote, verbose_name='投票情况')  # 通过GenericRelation关联到Vote表

    class Meta:
        ordering = ('-is_accepted', '-created_at')  # 多字段排序
        verbose_name = '答案'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, is_notify=True):
        super(Answer, self).save()
        # 避免二次通知
        if is_notify:
            # 通知提问者
            notification_handler(self.user, self.question.user, 'A', self.question)

    def get_markdown(self):
        return markdownify(self.content)

    def get_upvoters(self):
        """赞同的用户"""
        return [vote.user for vote in self.votes.filter(value=True)]

    def get_downvoters(self):
        """反对的用户"""
        return [vote.user for vote in self.votes.filter(value=False)]

    def total_votes(self):
        """得票数: 赞成票-反对票"""
        # return len(self.get_upvoters())-len(self.get_downvoters())
        dic = Counter(self.votes.values_list('value', flat=True))  # Counter赞同票多少，反对票少数
        return dic[True] - dic[False]

    def accept_answer(self):
        """接受回答"""
        # 当一个问题有多个回答的时候，只能采纳一个回答，其它回答一律置为未接受
        answer_set = Answer.objects.filter(question=self.question)  # 查询当前问题的所有回答
        answer_set.update(is_accepted=False)  # 一律置为未接受
        # 接受当前回答并保存
        self.is_accepted = True
        self.save(is_notify=False)
        # 该问题已有被接受的回答，保存
        self.question.has_correct = True
        self.question.save()
