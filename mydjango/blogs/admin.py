from django.contrib import admin

from mydjango.blogs.models import ArticleCategory, Article  # 必须加包名


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['catname', 'created_at', 'updated_at']  # admin中显示的字段


class ArticleAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    #     models.TextField: {'widget': MDEditorWidget}
    # }
    list_display = ['slug', 'title', 'user', 'category', 'status', 'tags', 'created_at']  # admin中显示的字段


# 注册
admin.site.register(ArticleCategory, ArticleCategoryAdmin)

admin.site.register(Article, ArticleAdmin)
