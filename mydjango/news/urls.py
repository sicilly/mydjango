from django.urls import path

from mydjango.news import views

app_name = "news"

urlpatterns = [
    path("", views.NewsListView.as_view(), name="list")
]
