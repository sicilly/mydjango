from django.urls import path
from django.views.generic import TemplateView

from mydjango.chat import views

app_name = "chat"
urlpatterns = [
    path('', views.MessagesListView.as_view(), name="index"),
    path('<str:username>/', views.ConversationListView.as_view(), name="conversation_detail"),
    path('send-message/', views.send_message, name="send_message"),
]
