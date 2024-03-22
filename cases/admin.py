from django.contrib import admin
from .models import Case, Comment, FollowUp, Picasso


class FollowUpInline(admin.TabularInline):  # new
    model = FollowUp
    extra = 0

class CommentInline(admin.TabularInline):  # new
    model = Comment
    extra = 0

class CaseAdmin(admin.ModelAdmin):  # new
    inlines = [
        FollowUpInline,
        CommentInline,
    ]
    list_display = [
    "title", "author","date_created","verified"
    ]

class PicassoAdmin(admin.ModelAdmin):
    list_display = [
    "title", "author","verified","date_created"
    ]

admin.site.register(Case, CaseAdmin)
admin.site.register(Picasso,PicassoAdmin)
admin.site.register(FollowUp)
admin.site.register(Comment)

