from django.conf import settings
from django.conf.urls import url
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),


    # path("quora/", TemplateView.as_view(template_name="pages/quora.html"), name="quora"),
    # path("chat/", TemplateView.as_view(template_name="pages/chat.html"), name="chat"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),

    # 第三方APP的路由
    re_path(r'mdeditor/', include('mdeditor.urls')),
    re_path(r'^comments/', include('django_comments.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('search/', include('haystack.urls')),

    # User management 用户管理
    path("users/", include("mydjango.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),

    # 我们自己写的App
    path("news/", include("mydjango.news.urls", namespace="news")),
    path("blogs/", include("mydjango.blogs.urls", namespace="blogs")),
    path("quora/", include("mydjango.quora.urls", namespace="quora")),
    path("chat/", include("mydjango.chat.urls", namespace="chat")),
    path("notifications/", include("mydjango.notifications.urls", namespace="notifications")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
