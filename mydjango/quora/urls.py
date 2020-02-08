from django.urls import path

from mydjango.quora import views

app_name = "quora"
urlpatterns = [
    path('', views.QuestionListView.as_view(), name="all-questions"),
    path('correct-answered-questions', views.CorrectAnsweredQuestionListView.as_view(), name="correct-answered-questions"),
    path('uncorrect-answered-questions', views.UncorrectAnsweredQuestionListView.as_view(),
         name="uncorrect-answered-questions"),
    path('ask-question/', views.QuestionCreateView.as_view(), name="ask_question")
]
