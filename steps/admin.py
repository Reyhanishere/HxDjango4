from django.contrib import admin
from .models import *
from .forms import *

from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicInlineSupportMixin,
    StackedPolymorphicInline
)
class TextBlockInline(StackedPolymorphicInline.Child):
    model = TextBlock

class ImageBlockInline(StackedPolymorphicInline.Child):
    model = ImageBlock

class MCQBlockInline(StackedPolymorphicInline.Child):
    model = MCQBlock

class KeyFeatureBlockInline(StackedPolymorphicInline.Child):
    model = KeyFeatureBlock

class PairingBlockInline(StackedPolymorphicInline.Child):
    model = PairingBlock

class MonoTextCheckBlockInline(StackedPolymorphicInline.Child):
    model = MonoTextCheckBlock

class BlockInline(StackedPolymorphicInline):
    model = Block
    child_inlines = (
        TextBlockInline,
        ImageBlockInline,
        MCQBlockInline,
        KeyFeatureBlockInline,
        PairingBlockInline,
        MonoTextCheckBlockInline,
    )
    extra = 1  # Number of empty forms shown by default
    sortable_field_name = "order"  # So you can reorder them easily if you have this field
# === Step & Field Admin ===
@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Step)
class StepAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    list_display = ('title', 'field', 'slug')
    list_filter = ('field',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlockInline]
# === Base Child Admin for All Blocks ===
class BlockChildAdmin(PolymorphicChildModelAdmin):
    base_model = Block

# === Individual Block Admins ===
@admin.register(TextBlock)
class TextBlockAdmin(BlockChildAdmin):
    base_model = TextBlock

@admin.register(ImageBlock)
class ImageBlockAdmin(BlockChildAdmin):
    base_model = ImageBlock

@admin.register(MCQBlock)
class MCQBlockAdmin(BlockChildAdmin):
    base_model = MCQBlock

@admin.register(KeyFeatureBlock)
class KeyFeatureBlockAdmin(BlockChildAdmin):
    base_model = KeyFeatureBlock

@admin.register(PairingBlock)
class PairingBlockAdmin(BlockChildAdmin):
    base_model = PairingBlock

@admin.register(MonoTextCheckBlock)
class MonoTextCheckBlockAdmin(BlockChildAdmin):
    base_model = MonoTextCheckBlock

# === Parent Block Admin ===

@admin.register(Block)
class BlockAdmin(PolymorphicParentModelAdmin):
    base_model = Block
    child_models = (
        TextBlock,
        ImageBlock,
        MCQBlock,
        KeyFeatureBlock,
        PairingBlock,
        MonoTextCheckBlock,
    )
    # readonly_fields = ('order',)
class RecordInline(admin.TabularInline):
    model=Record
    extra=0

# @admin.action(description="Clean Race Records")
# def clean_race_records(Race, request, queryset):
#     queryset.update(verified=False)

class RaceAdmin(admin.ModelAdmin):
    inlines = [RecordInline]
    # actions = [clean_race_records]

class CourseAdmin(admin.ModelAdmin):
    list_display=['title', 'professor',]

class CourseRegAdmin(admin.ModelAdmin):
    list_display=['course', 'student', 'joined_at']

class RecordAdmin(admin.ModelAdmin):
    list_display=['race', 'course', 'user', 'name', 'score']

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseRegistration, CourseRegAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Record, RecordAdmin)

# --------------------------- #
# ---- Interactive Steps ---- #
# --------------------------- #

class InteractiveTextOptionInline(StackedPolymorphicInline.Child):
    model = InteractiveTextOption

class InteractiveImageOptionInline(StackedPolymorphicInline.Child):
    model = InteractiveImageOption

class InteractiveOptionInline(StackedPolymorphicInline):
    model = InteractiveOption
    child_inlines = [InteractiveTextOptionInline, InteractiveImageOptionInline]
    fk_name = 'question'  # Important: set correct FK name

class InteractiveQuestionBlockAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    inlines = [InteractiveOptionInline]

# Optional: Register other block types
@admin.register(InteractiveImageBlock)
class InteractiveImageBlockAdmin(admin.ModelAdmin):
    pass

@admin.register(InteractiveTextBlock)
class InteractiveTextBlockAdmin(admin.ModelAdmin):
    pass

@admin.register(InteractiveQuestionBlock)
class InteractiveQuestionBlockAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    inlines = [InteractiveOptionInline]
    fk_name = "question block"

class InteractiveTextBlockInline(StackedPolymorphicInline.Child):
    model = InteractiveTextBlock

class InteractiveImageBlockInline(StackedPolymorphicInline.Child):
    model = InteractiveImageBlock

class InteractiveQuestionBlockInline(StackedPolymorphicInline.Child):
    model = InteractiveQuestionBlock
    inlines = [InteractiveOptionInline]

class InteractiveBlockInline(StackedPolymorphicInline):
    model = InteractiveBlock
    child_inlines = [InteractiveTextBlockInline, InteractiveImageBlockInline, InteractiveQuestionBlockInline]
    fk_name = 'step'

@admin.register(InteractiveStep)
class InteractiveStepAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    inlines = [InteractiveBlockInline]

@admin.register(InteractiveBlock)
class InteractiveBlockAdmin(PolymorphicParentModelAdmin):
    base_model = InteractiveBlock
    child_models = (InteractiveQuestionBlock, InteractiveImageBlock, InteractiveTextBlock)
    fk_name = "block"
    


