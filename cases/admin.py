from django.contrib import admin
from .models import (
    Case,
    Comment,
    FollowUp,
    Picasso,
    Note,
    Choice,
    Tag,
    # LabTestItem,
    ImageCase,
    Suggest,
    Rotation,
    Reply
)


class FollowUpInline(admin.TabularInline):
    model = FollowUp
    extra = 0


class CommentInline(admin.TabularInline):  # new
    model = Comment
    extra = 0

class ReplyInline(admin.TabularInline):
    model=Reply
    extra=0

# class LabInline(admin.TabularInline):
#     model = LabTestItem
#     extra = 1


class CaseImageInline(admin.TabularInline):
    model = ImageCase
    extra = 1

@admin.action(description="Deverify selected cases")
def deverify_case(Case, request, queryset):
    queryset.update(verified=False)

@admin.action(description="Verify selected cases")
def verify_case(Case, request, queryset):
    queryset.update(verified=True)

class CaseAdmin(admin.ModelAdmin):  # new
    inlines = [FollowUpInline, CommentInline, CaseImageInline]
    list_display = ["title", "author", "date_created", "verified","visible"]
    actions = [verify_case,deverify_case]

class CommentsAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]

class PicassoAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "verified", "delete", "date_created"]


@admin.action(description="Deverify selected notes")
def deverify_note(Case, request, queryset):
    queryset.update(verified=False)

@admin.action(description="Verify selected notes")
def verify_note(Case, request, queryset):
    queryset.update(verified=True)

class NotesAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "verified", "delete", "date_created"]
    actions=[verify_note,deverify_note]



admin.site.register(Choice)
admin.site.register(Tag)
admin.site.register(ImageCase)
admin.site.register(Suggest)
admin.site.register(Rotation)
admin.site.register(Case, CaseAdmin)
admin.site.register(Picasso, PicassoAdmin)
admin.site.register(Note,NotesAdmin)
# admin.site.register(FollowUp)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Reply)

# admin.site.register(LabTestItem)


