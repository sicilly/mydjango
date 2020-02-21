import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.db import models
from slugify import slugify


class NotificationQuerySet(models.query.QuerySet):
    def unread(self):
        return self.filter(unread=True)

    def read(self):
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):
        """标记已读，可以传入接收者参数"""
        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)
        return qs.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        """标为未读，可以传入接收者参数"""
        qs = self.read()
        if recipient:
            qs = qs.filter(recipient=recipient)
        return qs.update(unread=True)

    def get_most_recent(self, recipient=None):
        qs = self.unread()[:5]
        if recipient:
            qs = qs.filter(recipient=recipient)[:5]
        return qs

    def serialize_latest_notifications(self, recipient=None):
        """序列化最近5条未读通知，可以传入接收者参数"""
        qs = self.get_most_recent(recipient)
        notification_dic = serializers.serialize('json', qs)
        return notification_dic


class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('L', '赞了'),  # like
        ('C', '评论了'),  # comment
        ('F', '收藏了'),  # favor
        ('A', '回答了'),  # answer
        ('W', '接受了回答'),  # accept
        ('R', '回复了'),  # reply
        ('I', '登录'),  # logged in
        ('O', '退出'),  # logged out
    )
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notify_actor",
                              on_delete=models.CASCADE,verbose_name="触发者")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=False,
                                  related_name='notifications',on_delete=models.CASCADE, verbose_name='接收者')
    unread = models.BooleanField(default=True, db_index=True, verbose_name='未读')
    slug = models.SlugField(max_length=80, null=True, blank=True, verbose_name='(URL)别名')
    verb = models.CharField(max_length=1, choices=NOTIFICATION_TYPE, verbose_name='通知类别')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # GenericForeignKey设置
    content_type = models.ForeignKey(ContentType, related_name='notify_action_object', on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)  # 关联到整形和非整形的逐渐上，用CharField
    action_object = GenericForeignKey('content_type', 'object_id')  # 等同于GenericForeignKey()

    class Meta:
        verbose_name = "通知"
        verbose_name_plural = verbose_name
        ordering = ("-created_at",)

    # 要返回哪个用户做了什么事情
    def __str__(self):
        if self.action_object:
            return f'{self.actor}{self.get_verb_display()}{self.action_object}'
        return f'{self.actor}{self.get_verb_display()}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            self.slug = slugify(f'{self.recipient} {self.uuid_id} {self.verb}')
        super(Notification, self).save()

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()
