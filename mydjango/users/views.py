from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


# 详情视图
class UserDetailView(LoginRequiredMixin, DetailView):

    model = User  # 指定用户模型
    slug_field = "username"  # 必须是唯一的
    slug_url_kwarg = "username"  # 和urls中的占位符一致，如果不写默认为slug
    # pk_url_kwarg = 'pk' # 也可以用主键来查询，默认是pk
    template_name = 'users/user_detail.html'


user_detail_view = UserDetailView.as_view()


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
