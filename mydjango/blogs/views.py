from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from mydjango.blogs.models import Article, ArticleCategory
from blogs.form import ArticleForm
from myutils import AuthorRequiredMixin


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


class DraftListView(ArticleListView):
    """复用ArticleListView 草稿箱文章列表"""
    def get_queryset(self, **kwargs):
        return Article.objects.get_drafts()


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """创建文章"""
    model = Article
    form_class = ArticleForm
    template_name_suffix = '_create_form'
    template_name = "blogs/../templates/quora/article_create_form.html"

    # 表单验证
    def form_valid(self, form):
        form.instance.user = self.request.user  # form.instance是article的对象实例
        return super(ArticleCreateView, self).form_valid(form)

    # 发表文章成功后跳转
    # success_url = reverse_lazy('blogs:list')

    # 发表文章成功后跳转 并提示创建成功的消息
    def get_success_url(self):
        message = "您的文章已创建成功！"  # Django框架中的消息闪现机制
        messages.success(self.request, message)  # 消息传递给下一次请求
        return reverse_lazy('blogs:list')  # 返回到列表页


class ArticleDetailView(DetailView):
    """文章详情"""
    model = Article
    template_name = 'blogs/article_detail.html'
    context_object_name = 'article'


class ArticleUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """用户更新文章 需要登录"""
    model = Article
    form_class = ArticleForm
    template_name_suffix = '_update_form'
    template_name = "blogs/article_update_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleUpdateView, self).form_valid(form)

    # success_url = reverse_lazy('blogs:list')
    def get_success_url(self):
        message = "您的文章已更新成功！"  # Django框架中的消息闪现机制
        messages.success(self.request, message)  # 消息传递给下一次请求
        return reverse_lazy('blogs:detail', kwargs={'slug': self.get_object().slug})  # 传入路由的关键字参数
