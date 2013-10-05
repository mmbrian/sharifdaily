from django.contrib import admin
from .models import Report, Article, ArticleComment, ReportComment, Archive

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('view_count',)

class CommentAdmin(admin.ModelAdmin):
    # readonly_fields = ('author', 'created')
    readonly_fields = ('created',)

admin.site.register(Report, PostAdmin)
admin.site.register(Article, PostAdmin)
admin.site.register(ArticleComment, CommentAdmin)
admin.site.register(ReportComment, CommentAdmin)
admin.site.register(Archive)