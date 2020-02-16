from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from mydjango.chat.models import Message


class MessagesListView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'message_list'  # 模板中用到
    template_name = "chat/message_list.html"

    def get_queryset(self):
        """最近私信互动的内容"""
        # 获取最后一次联系的用户（激活用户）
        active_user = Message.objects.get_most_recent_conversation_user(self.request.user)
        # 返回当前登录用户和激活用户之间的消息
        return Message.objects.get_conversation(self.request.user, active_user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MessagesListView, self).get_context_data()
        # 获取除当前登录用户外的前10个用户，按最近登录时间降序排列
        context["users_list"] = get_user_model().objects.filter(is_active=True).exclude(username=self.request.user.username).order_by('-last_login')[0:10]

        # 最近一次私信互动的用户
        last_conversation_user = Message.objects.get_most_recent_conversation_user(self.request.user)
        context['active_user'] = last_conversation_user.username
        return context


class ConversationListView(MessagesListView):
    """与指定用户的私信内容"""
    def get_queryset(self):
        active_user = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        return Message.objects.get_conversation(active_user, self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ConversationListView, self).get_context_data()
        context['active_user'] = self.kwargs['username']
        return context
