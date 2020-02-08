from django.forms import ModelForm

from quora.models import Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["title", "status", "content", "tags"]
