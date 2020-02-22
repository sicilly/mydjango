from django.urls import path

from mydjango.notifications import views

app_name = "notifications"
urlpatterns = [
    path('', views.NotificationUnreadListView.as_view(), name="unread"),
    path('latest-notifications/', views.get_latest_notifications, name='latest_notifications'),
    path('mark-all-as-read', views.mark_all_as_read, name="mark_all_read"),
    path('mark-as-read/<slug>', views.mark_as_read, name="mark_as_read"),
]
