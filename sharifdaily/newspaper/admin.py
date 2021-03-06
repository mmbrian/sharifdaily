from django.contrib import admin
from .models import Report, Article, ArticleComment, ReportComment, Archive, Advertisement, Podcast

class PostAdmin(admin.ModelAdmin):
    list_display = ('headline', 'published', 'view_count', 'like_count', 'date')
    def like_count(self, obj):
        return unicode(obj.likes.count())
    like_count.short_description = 'Like count'

    readonly_fields = ('view_count', 'date')
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

class ReportAdmin(PostAdmin):
    list_display = ('headline', 'read', 'published', 'view_count', 'like_count', 'date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'read', 'is_public', 'created')

    readonly_fields = ('author', 'created')
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

class AdvertisementAdmin(admin.ModelAdmin):
    exclude = ('tag',)

class PodcastAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(Report, ReportAdmin)
admin.site.register(Article, PostAdmin)
admin.site.register(ArticleComment, CommentAdmin)
admin.site.register(ReportComment, CommentAdmin)
admin.site.register(Archive, ArchiveAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Podcast, PodcastAdmin)