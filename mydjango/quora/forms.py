from django.forms import ModelForm
from markdownx.fields import MarkdownxFormField

from mydjango.quora.models import Question  # 要加上mydjango！


class QuestionForm(ModelForm):
    content = MarkdownxFormField()  # 问题表述改成用md来渲染

    class Meta:
        model = Question
        fields = ["title", "status", "tags"]
