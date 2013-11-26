from django.contrib import admin
from .models import Report, Article, ArticleComment, ReportComment, Archive, Ad

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('view_count',)
    exclude = ('tag',)
    actions = ['make_public']

    def make_public(self, request, queryset):
        rows_updated = queryset.update(published=True)
        if rows_updated == 1:
            message_bit = "1 post was"
        else:
            message_bit = "%s posts were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
    make_public.short_description = "Make selected items as published"


class CommentAdmin(admin.ModelAdmin):
    # readonly_fields = ('author', 'created')
    readonly_fields = ('created',)
    exclude = ('tag',)
    actions = ['make_public']

    def make_public(self, request, queryset):
        rows_updated = queryset.update(is_public=True)
        if rows_updated == 1:
            message_bit = "1 comment was"
        else:
            message_bit = "%s comments were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
    make_public.short_description = "Make selected comments as public"

class ArchiveAdmin(admin.ModelAdmin):
    # exclude = ('tag',)
    pass

class AdAdmin(admin.ModelAdmin):
    exclude = ('tag',)

admin.site.register(Report, PostAdmin)
admin.site.register(Article, PostAdmin)
admin.site.register(ArticleComment, CommentAdmin)
admin.site.register(ReportComment, CommentAdmin)
admin.site.register(Archive, ArchiveAdmin)
admin.site.register(Ad, AdAdmin)