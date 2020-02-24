import uuid

from django.contrib.auth import get_user_model
from django.db import models

from django.conf import settings
from mydjango.notifications.views import notification_handler


# 自定义查询管理集
class MessageQuerySet(models.query.QuerySet):

    def get_conversation(self, sender, reciever):
        """用户间的私信会话"""
        qs_one = self.filter(sender=sender, reciever=reciever)  # A发送给B的消息
        qs_two = self.filter(sender=reciever, reciever=sender)  # B发送给A的消息
        return qs_one.union(qs_two).order_by('created_at')  # 取并集后按时间排序

    def get_most_recent_conversation_user(self, reciever):
        """获取最近一次私信互动的用户"""
        try:
            qs_sent = self.filter(sender=reciever)  # 当前登录用户发送的消息
            qs_received = self.filter(reciever=reciever)  # 当前登录用户接收的消息
            qs = qs_sent.union(qs_received).latest("created_at")  # 取并集后 最后一条消息
            if qs.sender == reciever:
                # 如果登录用户有发送消息，返回消息的接收者
                return qs.reciever
            # 否则返回消息的发送者
            return qs.sender
        except self.model.DoesNotExist:
            # 如果模型实例不存在，则返回当前用户
            return get_user_model().objects.get(username=reciever.username)


class Message(models.Model):
    """用户间私信"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages',
                               blank=True, null=True, on_delete=models.SET_NULL, verbose_name='发送者')
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages',
                                  blank=True, null=True, on_delete=models.SET_NULL, verbose_name='接收者')
    message = models.TextField(blank=True, null=True, verbose_name='内容')
    unread = models.BooleanField(default=True, db_index=True, verbose_name='是否未读')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 没有updated_at，私信发送之后不能修改或撤回
    objects = MessageQuerySet.as_manager()  # 注册模型管理器

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        return self.message  # 返回消息内容

    def mark_as_read(self):
        if self.unread:
            self.unread = False  # 置为已读
            self.save()

    def save(self, force_insert=False, force_update=False, using=None,
                 update_fields=None):
        super(Message, self).save()
        # 通知被私信者
        notification_handler(self.sender, self.reciever, 'M', self)
