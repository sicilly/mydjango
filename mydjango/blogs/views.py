from django.views.generic import ListView, CreateView, DetailView, UpdateView

from mydjango.blogs.models import Article, ArticleCategory


class ArticleListView(ListView):
    """已发布的文章列表"""
    model = Article
    paginate_by = 5
    context_object_name = 'article_list'
    template_name = "blogs/article_list.html"

    def get_queryset(self, **kwargs):
        return Article.objects.get_published()

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        context['article_categories'] = ArticleCategory.objects.all()
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context
