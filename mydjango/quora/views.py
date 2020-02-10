from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, DetailView

from mydjango.quora.models import Question, Answer
from mydjango.quora.forms import QuestionForm
from mydjango.myutils import ajax_required


class QuestionListView(ListView):
    """所有问题页"""
    model = Question
    paginate_by = 20
    context_object_name = 'question_list'  # 上下文变量 不要用"-"号
    template_name = 'quora/question_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
        context["popular_tags"] = Question.objects.get_counted_tags()
        context["active"] = "all"
        return context


class CorrectAnsweredQuestionListView(QuestionListView):
    """已有采纳答案的问题列表"""
    def get_queryset(self):
        return Question.objects.get_correct_answered()

    def get_context_data(self, *, object_list=None, **kwargs):
        """ 通过传递context["active"]的值来判断点击了哪个tab从而改变前端样式 """
        context = super(CorrectAnsweredQuestionListView, self).get_context_data()
        context["active"] = "correct_answered"
        return context


class UncorrectAnsweredQuestionListView(QuestionListView):
    """未有采纳答案的问题列表"""
    def get_queryset(self):
        return Question.objects.get_uncorrect_answered()

    def get_context_data(self, *, object_list=None, **kwargs):
        """ 通过传递context["active"]的值来判断点击了哪个tab从而改变前端样式 """
        context = super(UncorrectAnsweredQuestionListView, self).get_context_data()
        context["active"] = "uncorrect_answered"
        return context


class QuestionCreateView(LoginRequiredMixin, CreateView):
    """用户提问"""
    model = Question
    form_class = QuestionForm
    template_name_suffix = '_create_form'
    template_name = 'quora/question_create_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "问题已提交！")
        return reverse_lazy("quora:all-questions")


class QuestionDetailView(DetailView):
    """问题详情页"""
    model = Question
    context_object_name = 'question'
    template_name = 'quora/question_detail.html'
    query_pk_and_slug = True  # 同时用上pk和slug，保证url的唯一性和可读性
    slug_url_kwarg = 'slug'  # 默认就是slug

    # def get_context_data(self, **kwargs):
    #     context['answers'] = Answer.objects.filter(question=self.get_object())


class AnswerCreateView(LoginRequiredMixin, CreateView):
    """回答问题"""
    model = Answer
    fields = ['content', ]
    template_name_suffix = '_create_form'
    template_name = 'quora/answer_create_form.html'

    def get_context_data(self, **kwargs):
        context = super(AnswerCreateView, self).get_context_data()
        context["question"] = Question.objects.get(pk=self.kwargs['question_id'])
        return context  # 得返回啊！

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(AnswerCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "回答已提交！")
        return reverse_lazy("quora:question_detail", kwargs={"pk": self.kwargs['question_id'],
                                                             "slug": self.kwargs['question_slug']})


@login_required
@ajax_required
@require_http_methods(["POST"])
def question_vote(request):
    """给问题投票，AJAX POST请求"""
    question_id = request.POST["questionId"]
    value = True if request.POST["value"] == 'U' else False  # 'U'表示赞成，'D'表示反对
    question = Question.objects.get(pk=question_id)
    users = question.votes.values_list('user', flat=True)  # 当前问题的所有投票用户
    if request.user.pk in users and (question.votes.get(user=request.user).value == value):
        question.votes.get(user=request.user).delete()
    else:
        question.votes.update_or_create(user=request.user, defaults={"value": value})
    return JsonResponse({"votes": question.total_votes()})  # 返回响应
