from functools import wraps

from django.http import HttpResponseBadRequest


def ajax_required(f):
    """验证是否为AJAX请求"""

    @wraps(f)
    def wrap(request, *args, **kwargs):
        #  request.is_ajax() 方法判断是否是 ajax 请求
        # 参考:https://code.ziqiangxuetang.com/django/django-ajax.html
        if not request.is_ajax():
            return HttpResponseBadRequest("不是AJAX请求！")
        return f(request, *args, **kwargs)

    return wrap
