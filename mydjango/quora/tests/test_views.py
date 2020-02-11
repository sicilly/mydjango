import json

from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from test_plus.test import CBVTestCase

from mydjango.quora.models import Question, Answer
from mydjango.quora import views


class BaseQATest(CBVTestCase):

    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")
        self.question_one = Question.objects.create(
            user=self.user,
            title="问题1",
            content="问题1的内容",
            tags="测试1, 测试2"
        )
        self.question_two = Question.objects.create(
            user=self.user,
            title="问题2",
            content="问题2的内容",
            has_correct=True,
            tags="测试1, 测试2"
        )
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question_two,
            content="问题2被采纳的回答",
            is_accepted=True
        )

        self.request = RequestFactory().get('/fake-url')
        self.request.user = self.user  # 登录


class TestQuestionListView(BaseQATest):
    """测试问题列表视图"""
    def test_get_context_data(self):
        response = self.get(views.QuestionListView, request=self.request)

        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context_data['question_list'],
                                 map(repr, [self.question_one, self.question_two]),
                                 ordered=False)

        self.assertContext('active', 'all')

        self.assertContext('popular_tags', Question.objects.get_counted_tags())


class TestCorrectAnsweredQuestionListView(BaseQATest):
    """测试已有正确答案的问题列表"""
    def test_get_context_data(self):
        response = self.get(views.CorrectAnsweredQuestionListView, request=self.request)  # 方式一
        # response = views.CorrectAnsweredQuestionListView.as_view()(self.request) # 方式二

        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context_data['question_list'], [repr(self.question_two)])

        self.assertContext('active', 'correct_answered')  # 对应方式一
        # self.assertEqual(response.context_data['active'], 'correct_answered')  # 对应方式二


class TestUncorrectAnsweredQuestionListView(BaseQATest):
    """测试没有正确答案的问题列表"""

    def test_get_context_data(self):
        response = self.get(views.UncorrectAnsweredQuestionListView, request=self.request)  # 方式一
        self.assertEqual(response.status_code, 200)  # 或者 self.response_200(response)
        self.assertQuerysetEqual(response.context_data['question_list'], [repr(self.question_one)])
        self.assertContext('active', 'uncorrect_answered')


class TestQuestionCreateView(BaseQATest):
    """测试创建问题"""

    def test_get(self):
        response = self.get(views.QuestionCreateView, request=self.request)
        self.response_200(response)

        self.assertContains(response, '标题')
        self.assertContains(response, '编辑')
        self.assertContains(response, '预览')
        self.assertContains(response, '标签')

        self.assertIsInstance(response.context_data['view'], views.QuestionCreateView)

    def test_post(self):
        data = {'title': 'title', 'content': 'content', 'tags': 'tag1,tag2', 'status': 'O'}  # 准备数据
        request = RequestFactory().post('/fake-url', data=data)  # 提交数据
        request.user = self.user  # 登录

        # RequestFactory测试含有django.contrib.messages的视图 https://code.djangoproject.com/ticket/17971
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = self.post(views.QuestionCreateView, request=request)
        assert response.status_code == 302  # 重定向
        assert response.url == '/quora/'


class TestQuestionDetailView(BaseQATest):
    """测试问题详情"""

    def test_context_data(self):
        response = self.get(views.QuestionDetailView, request=self.request,
                            pk=self.question_one.pk, slug=self.question_one.slug)
        self.response_200(response)
        self.assertEqual(response.context_data['question'], self.question_one)


class TestAnswerCreateView(BaseQATest):
    """测试创建回答"""

    def test_get(self):
        response = self.get(views.AnswerCreateView, request=self.request,
                            question_id=self.question_one.id,
                            question_slug=self.question_one.slug)
        self.response_200(response)

        self.assertContains(response, '编辑')
        self.assertContains(response, '预览')
        self.assertIsInstance(response.context_data['view'], views.AnswerCreateView)

    def test_post(self):
        data = {'content': 'content'}
        request = RequestFactory().post('/fake-url', data=data)
        request.user = self.user

        # RequestFactory测试含有django.contrib.messages的视图 https://code.djangoproject.com/ticket/17971
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = self.post(views.AnswerCreateView, request=request, question_id=self.question_one.pk,
                             question_slug=self.question_one.slug)

        assert response.status_code == 302
        assert response.url == f'/quora/question/{self.question_one.pk}/{self.question_one.slug}/'


class TestQAVote(BaseQATest):

    def setUp(self):
        super(TestQAVote, self).setUp()
        self.request = RequestFactory().post('/fake-url', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # QueryDict instance is immutable, request.POST是QueryDict对象，不可变
        self.request.POST = self.request.POST.copy()
        self.request.user = self.other_user

    def test_question_upvote(self):
        """赞同问题"""
        self.request.POST['questionId'] = self.question_one.pk

        self.request.POST['value'] = 'U'

        response = views.question_vote(self.request)

        assert response.status_code == 200
        assert json.loads(response.content)['votes'] == 1

    def test_question_downvote(self):
        """反对问题"""
        self.request.POST['questionId'] = self.question_one.pk

        self.request.POST['value'] = 'D'

        response = views.question_vote(self.request)

        assert response.status_code == 200
        assert json.loads(response.content)['votes'] == -1

    def test_answer_upvote(self):
        """赞同答案"""
        self.request.POST['answerId'] = self.answer.uuid_id
        self.request.POST['value'] = 'U'

        response = views.answer_vote(self.request)

        assert response.status_code == 200
        assert json.loads(response.content)['votes'] == 1

    def test_answer_downvote(self):
        """反对答案"""
        self.request.POST['answerId'] = self.answer.uuid_id
        self.request.POST['value'] = 'D'

        response = views.answer_vote(self.request)

        assert response.status_code == 200
        assert json.loads(response.content)['votes'] == -1

    def test_accept_answer(self):
        """接受回答"""
        self.request.user = self.user  # self.user是提问者
        self.request.POST['answerId'] = self.answer.pk

        response = views.accept_answer(self.request)

        assert response.status_code == 200
        assert json.loads(response.content)['status'] == 'true'
