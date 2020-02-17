from django.urls import path

from mydjango.chat import views

app_name = 'chat'

urlpatterns = [
    path('', views.MessagesListView.as_view(), name="index"),
    path('send-message/', views.send_message, name="send_message"),  # 改了这俩顺序
    path('<str:username>/', views.ConversationListView.as_view(), name="conversation_detail"),  # 改了这俩顺序
]
