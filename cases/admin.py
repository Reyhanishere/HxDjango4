from django.contrib import admin
from .models import *

class CommentInline(admin.TabularInline):  # new
    model = Comment
    extra = 0

class ReplyInline(admin.TabularInline):
    model=Reply
    extra=0

class CaseImageInline(admin.TabularInline):
    model = ImageCase
    extra = 1
    
class LabGraphInline(admin.TabularInline):
    model=LabGraphSelection
    extra=1

class CaseMessageInline(admin.TabularInline):
    model = CaseMessage
    extra=1

@admin.action(description="Deverify selected cases")
def deverify_case(Case, request, queryset):
    queryset.update(verified=False)

@admin.action(description="Verify selected cases")
def verify_case(Case, request, queryset):
    queryset.update(verified=True)

class CaseAdmin(admin.ModelAdmin):  # new
    inlines = [CommentInline, CaseImageInline, LabGraphInline, CaseMessageInline]
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

class AIRRLAdmin(admin.ModelAdmin):
    list_display=["request_content", "ai_model", "user"]

admin.site.register(Choice)
admin.site.register(Tag)
admin.site.register(ImageCase)
admin.site.register(Suggest)
admin.site.register(Rotation)
admin.site.register(CaseMessage)
admin.site.register(Case, CaseAdmin)
admin.site.register(Picasso, PicassoAdmin)
admin.site.register(Note,NotesAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Reply)
admin.site.register(LabGraphSelection)
admin.site.register(AIReqResLog,AIRRLAdmin)
