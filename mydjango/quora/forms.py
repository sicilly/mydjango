from django.forms import ModelForm

from mydjango.quora.models import Question  # 要加上mydjango！


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["title", "status", "content", "tags"]
