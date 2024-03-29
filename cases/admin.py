from django.contrib import admin
from .models import (
    Case,
    Comment,
    FollowUp,
    Picasso,
    Choice,
    Tag,
    LabTestItem,
    CaseImage,
)


class FollowUpInline(admin.TabularInline):
    model = FollowUp
    extra = 0


class CommentInline(admin.TabularInline):  # new
    model = Comment
    extra = 0


class LabInline(admin.TabularInline):
    model = LabTestItem
    extra = 1


class CaseImageInline(admin.TabularInline):
    model = CaseImage
    extra = 1


class CaseAdmin(admin.ModelAdmin):  # new
    inlines = [FollowUpInline, CommentInline, LabInline, CaseImageInline]
    list_display = ["title", "author", "date_created", "verified"]


class PicassoAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "verified", "date_created"]


admin.site.register(Choice)
admin.site.register(Tag)
admin.site.register(Case, CaseAdmin)
admin.site.register(Picasso, PicassoAdmin)
# admin.site.register(FollowUp)
admin.site.register(Comment)
# admin.site.register(LabTestItem)
admin.site.register(CaseImage)
