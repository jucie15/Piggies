from django.contrib import admin
from cast.models import *

class CommentInline(admin.StackedInline):
    model = Comment

@admin.register(Contents)
class ContentsAdmin(admin.ModelAdmin):
    model = Contents
    search_fields = ('tag', )
    inlines = [
        CommentInline,
    ]
    actions = ['delete_empty_contents']

    def delete_empty_contents(self, request, queryset):
        Contents.delete_empty_contents(queryset)
        self.message_user(request, "짤린 동영상 컨텐츠 삭제 성공.")
    delete_empty_contents.short_description = "짤린 동영상 컨텐츠를 삭제합니다."

class PledgeInline(admin.TabularInline):
    model = Pledge

@admin.register(Congressman)
class CongressmanAdmin(admin.ModelAdmin):
    model = Congressman
    search_fields = ('name', 'party', 'tag', )
    list_display = ['id', 'name', 'party', 'constituency', 'updated_at']
    inlines = [
        PledgeInline,
        CommentInline,
    ]
    list_display_links = ('id','name','party','constituency',)

@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    model = Pledge
    search_fields = ('tag', )
    inlines = [
        CommentInline,
    ]

class ReCommentInline(admin.StackedInline):
    model = ReComment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    inlines = [
        ReCommentInline,
    ]

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite

@admin.register(ContentsEmotion)
class ContentsEmotionAdmin(admin.ModelAdmin):
    model = ContentsEmotion

@admin.register(CommentEmotion)
class CommentEmotionAdmin(admin.ModelAdmin):
    model = CommentEmotion

# admin.site.register(Contents)
# admin.site.register(Congressman)
# admin.site.register(Pledge)
# admin.site.register(ContentsEmotion)
# admin.site.register(PledgeEmotion)
# admin.site.register(CongressmanEmotion)
# admin.site.register(Comment)
# admin.site.register(CommentEmotion)
# admin.site.register(ReComment)
