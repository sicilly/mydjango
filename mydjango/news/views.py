from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView

from mydjango.news.models import News
from mydjango.myutils import ajax_required, AuthorRequiredMixin


class NewsListView(ListView):
    """新闻列表页"""
    model = News
    queryset = News.objects.filter(reply=False).all()  # 过滤出新闻（也可重写get_queryset函数)
    paginate_by = 10
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'

    def get_queryset(self, *kwargs):
        return News.objects.filter(reply=False).all()


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_news(request):
    """发送动态，AJAX POST请求"""
    newsContent = request.POST['news_content'].strip()
    if newsContent:
        news = News.objects.create(user=request.user, content=newsContent)
        html = render_to_string('news/news_single.html', {'news': news, 'request': request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不能为空！")


class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """删除一条新闻记录"""
    model = News
    # template_name_suffix = '_confirm_delete'
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news:list')  # 在项目的URLConf未加载前使用


@login_required
@ajax_required
@require_http_methods(["POST"])
def like(request):
    """点赞，响应AJAX POST请求"""
    news_id = request.POST['newsId']
    news = News.objects.get(pk=news_id)
    # 取消或者添加赞
    news.switch_like(request.user)
    # 返回赞的数量
    return JsonResponse({"likers_count": news.likers_count()})


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_reply(request):
    """发送回复，AJAX POST请求"""
    replyContent = request.POST['replyContent'].strip()  # 接收回复内容
    parentId = request.POST['newsid']                    # 接收新闻id
    parent = News.objects.get(pk=parentId)               # 查数据库得到新闻
    if replyContent:
        parent.reply_this(request.user, replyContent)
        return JsonResponse({'newsid': parent.pk, 'replies_count': parent.replies_count()})  # 返回数据
    else:
        return HttpResponseBadRequest("内容不能为空！")
#
#
# @ajax_required
# @require_http_methods(["GET"])
# def get_replies(request):
#     """返回新闻的评论，AJAX GET请求"""
#     news_id = request.GET['newsId']
#     news = News.objects.get(pk=news_id)
#     # render_to_string()表示加载模板，填充数据，返回字符串
#     replies_html = render_to_string("news/reply_list.html", {"replies": news.get_children()})  # 有评论的时候
#     return JsonResponse({
#         "newsid": news_id,
#         "replies_html": replies_html,
#     })
