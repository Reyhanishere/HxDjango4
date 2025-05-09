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

class BlockInline(StackedPolymorphicInline):
    model = Block
    child_inlines = (
        TextBlockInline,
        ImageBlockInline,
        MCQBlockInline,
        KeyFeatureBlockInline,
        PairingBlockInline,
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
    )
