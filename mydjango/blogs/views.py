from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from mydjango.blogs.models import Article, ArticleCategory
from blogs.form import ArticleForm


class ArticleListView(ListView):
    """已发布的文章列表"""
    model = Article
    paginate_by = 5     # 分页 一页5篇文章
    context_object_name = 'article_list'
    template_name = "blogs/article_list.html"

    def get_queryset(self, **kwargs):
        return Article.objects.get_published()

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        context['article_categories'] = ArticleCategory.objects.all()
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """创建文章"""
    model = Article
    form_class = ArticleForm
    template_name_suffix = '_form'
    template_name = "blogs/article_form.html"

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super(ArticleCreateView,self).form_valid(form)
    #
    # # success_url = reverse_lazy('blogs:list')
    # def get_success_url(self):
    #     message = "您的文章已创建成功！"  # Django框架中的消息闪现机制
    #     messages.success(self.request, message)  # 消息传递给下一次请求
    #     return reverse_lazy('blogs:list')
