from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from mydjango.blogs import views

app_name = "blogs"

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list"),
    path("article-create/", views.ArticleCreateView.as_view(), name="create"),
    path("get-drafts/", views.DraftListView.as_view(), name="drafts"),
    # path("article/<str:slug>/", views.ArticleDetailView.as_view(), name="detail"),
    path("article/<str:slug>/", cache_page(5*60)(views.ArticleDetailView.as_view()), name="detail"),
    path("article-update/<int:pk>/", views.ArticleUpdateView.as_view(), name="update"),
]
