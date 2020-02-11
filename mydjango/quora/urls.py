from django.urls import path

from mydjango.quora import views

app_name = "quora"
urlpatterns = [
    path('', views.QuestionListView.as_view(), name="all-questions"),
    path('correct-answered-questions', views.CorrectAnsweredQuestionListView.as_view(), name="correct-answered-questions"),
    path('uncorrect-answered-questions', views.UncorrectAnsweredQuestionListView.as_view(),
         name="uncorrect-answered-questions"),
    path('ask-question/', views.QuestionCreateView.as_view(), name="ask_question"),
    path('question/<int:pk>/<str:slug>/', views.QuestionDetailView.as_view(), name="question_detail"),
    path('create-answer/<int:question_id>/<str:question_slug>/',
         views.AnswerCreateView.as_view(), name="create_answer"),
    path('question/vote/', views.question_vote, name="question_vote"),
    path('answer/vote/', views.answer_vote, name="answer_vote"),
]
