from django.urls import path

from mydjango.news import views

app_name = "news"

urlpatterns = [
    path("", views.NewsListView.as_view(), name="list"),
    path("post-news/", views.post_news, name='post_news'),
    path("delete/<str:pk>", views.NewsDeleteView.as_view(), name='delete_news'),
    path('like/', views.like, name="post_like"),
    path('post-reply/', views.post_reply, name="post_reply"),
    path('get-replies/', views.get_replies, name="get_replies"),
    path('update-interactions/', views.update_interactions, name="update_interactions"),


]
