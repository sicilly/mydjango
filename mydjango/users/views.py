from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from mydjango.blogs.models import Article
from mydjango.news.models import News
from mydjango.quora.models import Question, Answer

User = get_user_model()


# 详情视图
class UserDetailView(LoginRequiredMixin, DetailView):

    model = User  # 指定用户模型
    slug_field = "username"  # 必须是唯一的
    slug_url_kwarg = "username"  # 和urls中的占位符一致，如果不写默认为slug
    # pk_url_kwarg = 'pk' # 也可以用主键来查询，默认是pk
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data()
        user = self.get_object()
        context["articles_count"] = Article.objects.get_by_user(user).count()
        context["news_count"] = News.objects.filter(user=user, reply=False).count()
        context["questions_count"] = Question.objects.get_questions_by_user(user).count()
        context["answers_count"] = Answer.objects.filter(user=user).count()
        return context


user_detail_view = UserDetailView.as_view()


# 用户的博客文章
class UserArticlesDetailView(UserDetailView):
    def get_context_data(self, **kwargs):
        context = super(UserArticlesDetailView, self).get_context_data()
        context["articles"] = Article.objects.get_by_user(self.get_object())
        context["active"] = 'articles'
        return context


# 用户的新闻动态
class UserNewsDetailView(UserDetailView):
    def get_context_data(self, **kwargs):
        context = super(UserNewsDetailView, self).get_context_data()
        context["news"] = News.objects.filter(user=self.get_object(), reply=False).order_by('-updated_at')
        context["active"] = 'news'
        return context


# 用户的问题
class UserQuestionsDetailView(UserDetailView):
    def get_context_data(self, **kwargs):
        context = super(UserQuestionsDetailView, self).get_context_data()
        context["questions"] = Question.objects.get_questions_by_user(self.get_object())
        context["active"] = 'questions'
        return context


# 用户的回答
class UserAnswersDetailView(UserDetailView):
    def get_context_data(self, **kwargs):
        context = super(UserAnswersDetailView, self).get_context_data()
        context["answers"] = Answer.objects.filter(user=self.get_object())
        context["active"] = 'answers'
        return context


user_articles_detail_view = UserArticlesDetailView.as_view()
user_news_detail_view = UserNewsDetailView.as_view()
user_questions_detail_view = UserQuestionsDetailView.as_view()
user_answers_detail_view = UserAnswersDetailView.as_view()


# 更新视图
class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User  # 模型
    fields = ["nickname", "job", "introduction", "avatar", "address", "birthday",
              "personal_url", "weibo", "zhihu", "github", "linkedin"]  # 可更新的字段
    template_name = 'users/user_form.html'

    def get_success_url(self):  # 更新成功后跳转
        # kwargs里面的键"username"也是占位符
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):  # 获取当前登录的对象
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


# 重定向视图
class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):  # 获取重定向url
        # kwargs里面的键"username"也是占位符
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
