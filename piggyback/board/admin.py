from django.contrib import admin
from board.models import Feedback, BoardComment


class BoardCommentAdmin(admin.ModelAdmin):
    model = BoardComment

class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback


admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(BoardComment, BoardCommentAdmin)
