from django import forms
from mdeditor.fields import MDTextFormField

from mydjango.blogs.models import Article


class ArticleForm(forms.ModelForm):
    content = MDTextFormField()

    class Meta:
        model = Article
        # 希望用户填的字段
        fields = ["category", "title", "abstract", "content", "cover", "tags", "status"]
