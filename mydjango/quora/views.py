from django.views.generic import ListView

from mydjango.quora.models import Question


class QuestionListView(ListView):
    """所有问题页"""
    model = Question
    paginate_by = 20
    context_object_name = 'question-list'
    template_name = 'quora/question_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
        context["popular_tags"] = Question.objects.get_counted_tags()
        return context


class CorrectAnsweredQuestionListView(QuestionListView):
    """已有采纳答案的问题列表"""
    def get_queryset(self):
        return Question.objects.get_correct_answered()


class UncorrectAnsweredQuestionListView(QuestionListView):
    """未有采纳答案的问题列表"""
    def get_queryset(self):
        return Question.objects.get_uncorrect_answered()
