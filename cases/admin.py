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
    Roataion,
)


class FollowUpInline(admin.TabularInline):
    model = FollowUp
    extra = 0


class CommentInline(admin.TabularInline):  # new
    model = Comment
    extra = 0


# class LabInline(admin.TabularInline):
#     model = LabTestItem
#     extra = 1


class CaseImageInline(admin.TabularInline):
    model = ImageCase
    extra = 1


class CaseAdmin(admin.ModelAdmin):  # new
    inlines = [FollowUpInline, CommentInline, CaseImageInline]
    list_display = ["title", "author", "date_created", "verified","visible"]


class PicassoAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "verified", "delete", "date_created"]

class NotesAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "verified", "delete", "date_created"]



admin.site.register(Choice)
admin.site.register(Tag)
admin.site.register(ImageCase)
admin.site.register(Suggest)
admin.site.register(Rotation)
admin.site.register(Case, CaseAdmin)
admin.site.register(Picasso, PicassoAdmin)
admin.site.register(Note,NotesAdmin)
# admin.site.register(FollowUp)
admin.site.register(Comment)
# admin.site.register(LabTestItem)
