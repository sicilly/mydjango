from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    # blank=True表示前端提交时可以为空, null=True表示数据库里该字段可以为空
    nickname = models.CharField(verbose_name='用户昵称', blank=True, null=True, max_length=255, default='')
    job = models.CharField(verbose_name='用户职业', blank=True, null=True, max_length=50, default='未知')
    introduction = models.TextField(verbose_name='简介', blank=True, null=True, default='该用户很懒，什么都没留下')
    avatar = models.ImageField(verbose_name='头像', upload_to='users/avatars/', blank=True, null=True, default='')
    address = models.CharField(verbose_name='住址', blank=True, null=True, max_length=50, default='')
    birthday = models.DateField(verbose_name='生日', blank=True, null=True, default=timezone.now)
    personal_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='个人链接', default='')
    weibo = models.URLField(max_length=255, null=True, blank=True, verbose_name='微博链接', default='')
    zhihu = models.URLField(max_length=255, null=True, blank=True, verbose_name='知乎链接', default='')
    github = models.URLField(max_length=255, null=True, blank=True, verbose_name='GitHub链接', default='')
    linkedin = models.URLField(max_length=255, null=True, blank=True, verbose_name='LinkedIn链接', default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    # 前端界面显示用户信息 有昵称则返回昵称，否则返回用户名
    def get_profile_name(self):
        if self.nickname:
            return self.nickname
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
