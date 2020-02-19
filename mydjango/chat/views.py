from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from mydjango.chat.models import Message
from mydjango.myutils import ajax_required


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


@login_required
@ajax_required
@require_http_methods(["POST"])
def send_message(request):
    """发送消息，AJAX POST请求"""
    sender = request.user  # 发送者是当前登录用户
    reciever_username = request.POST['to']
    reciever = get_user_model().objects.get(username=reciever_username)
    msgcontent = request.POST['msgcontent']
    if len(msgcontent.strip()) != 0 and sender != reciever:
        msg = Message.objects.create(sender=sender, reciever=reciever, message=msgcontent)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'message': render_to_string('chat/message_single.html', {'message': msg}),
            'sender': sender.username,
        }
        # 异步变同步
        # group_send(group: 所在组-接收者的username, message: 消息内容)
        async_to_sync(channel_layer.group_send)(reciever.username, payload)
        return render(request, 'chat/message_single.html', {'message': msg})
    return HttpResponse()
