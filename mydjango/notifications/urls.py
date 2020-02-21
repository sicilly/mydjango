from django.urls import path

from mydjango.notifications import views

app_name = "notifications"
urlpatterns = [
    path('', views.NotificationUnreadListView.as_view(), name="unread"),
    path('latest-notifications/', views.get_latest_notifications, name='latest_notifications')
]
