from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from mydjango.notifications.models import Notification


class NotificationUnreadListView(LoginRequiredMixin, ListView):
    """未读通知列表"""
    model = Notification
    context_object_name = 'notification_list'
    template_name = 'notifications/notification_list.html'

    def get_queryset(self):
        return self.request.user.notifications.unread()


@login_required
def get_latest_notifications(request):
    """最近的未读通知"""
    notifications = request.user.notifications.get_most_recent()
    return render(request, 'notifications/most_recent.html',
                  {'notifications': notifications})
