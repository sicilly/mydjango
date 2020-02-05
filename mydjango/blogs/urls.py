from django.urls import path
from django.views.generic import TemplateView

from mydjango.blogs import views

app_name = "blogs"

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list"),
]
