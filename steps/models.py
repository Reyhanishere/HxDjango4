from django.db import models
from django.conf import settings
from django.utils import timezone

from polymorphic.models import PolymorphicModel

# === STEP & BLOCK SYSTEM ===
class Field(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title

class Race(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def is_open(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def __str__(self):
        return self.name

class Step(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True)
    race = models.ForeignKey(Race, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Block(PolymorphicModel):
    step = models.ForeignKey("Step", related_name="blocks", on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = ("step", "order")

    def __str__(self):
        return f"{self.step.title} - Block {self.order}"

# === BLOCK TYPES ===

class TextBlock(Block):
    visible = models.BooleanField(default=True)
    text = models.TextField()

    def __str__(self):
        return f"{self.text[:50]}"

def step_image_upload_path(instance, filename):
    step_slug = instance.step.slug
    return f'steps/{step_slug}/images/{filename}'

class ImageBlock(Block):
    visible = models.BooleanField(default=True)
    image = models.ImageField(upload_to=step_image_upload_path)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"{self.caption[:50]}"

class MCQBlock(Block):
    visible = models.BooleanField(default=True)
    question = models.TextField()
    choices = models.JSONField()
    correct_choice = models.CharField(max_length=10)
    explanation = models.TextField(blank=True)
    xp = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.question[:50]}"

class KeyFeatureBlock(Block):
    visible = models.BooleanField(default=True)
    question = models.TextField()
    all_features = models.JSONField()
    expected_features = models.JSONField()
    expected_features_count = models.PositiveIntegerField(default=0)
    explanation = models.TextField(blank=True)
    xp = models.IntegerField(default=10)

    def save(self, *args, **kwargs):
        if isinstance(self.expected_features, dict):
            self.expected_features_count = len(self.expected_features.keys())
        else:
            self.expected_features_count = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.question[:50]}"

class PairingBlock(Block):
    visible = models.BooleanField(default=True)
    prompt = models.TextField(blank=True, null=True)
    pairs = models.JSONField()
    explanation = models.TextField(blank=True)
    xp = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.prompt[:50]}"

# class SortingBlock(Block):
#     prompt = models.TextField(blank=True, null=True)
#     options = models.JSONField()
#     explanation = models.TextField(blank=True)
#     xp = models.IntegerField(default=10)
#     def __str__(self):
#         return f"{self.prompt[:50]}"

# class TextCheckBlock(Block):
#     prompt = models.TextField(blank=True, null=True)
#     answer_list = models.TextField()
#     explanation = models.TextField(blank=True)
#     xp = models.IntegerField(default=10)
#     def __str__(self):
#         return f"{self.prompt[:50]}"

# === USER ANSWERS & PROGRESS ===

class UserAnswer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True)
    submitted_data = (
        models.JSONField()
    )  # Can store selected option, typed keywords, pairs, etc.
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user} to Block {self.block.id if self.block else 'Deleted Block'}"

class UserProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True)
    completed_blocks = models.ManyToManyField(Block, blank=True)
    xp = models.IntegerField(default=10)
    streak = models.IntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} progress in {self.step}"

class Record(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="records")
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    class Meta:
        unique_together = ("race", "name")

    def __str__(self):
        return f"{self.race}| {self.name}: {self.score}"

# --------------------------- #
# ---- Interactive Steps ---- #
# --------------------------- #

class InteractiveStep(Step):
    class Meta:
        verbose_name = "Interactive Step"

class InteractiveBlock(PolymorphicModel):
    step = models.ForeignKey(InteractiveStep, related_name="interactive_blocks", on_delete=models.CASCADE)
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('step', 'number')
        ordering = ['number']

class InteractiveQuestionBlock(InteractiveBlock):
    question_text = models.TextField()
    parse_md=models.BooleanField(default=False)
    image = models.ImageField(upload_to=step_image_upload_path, blank=True, null= True)
    image_alt_text = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"{self.step}: {self.question_text[:20]}"

class InteractiveTextBlock(InteractiveBlock):
    content = models.TextField()
    parse_md=models.BooleanField(default=False)
    next_block_number = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return f"{self.step}: {self.content[:20]}"

class InteractiveImageBlock(InteractiveBlock):
    image = models.ImageField(upload_to=step_image_upload_path)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    caption = models.TextField(blank=True)
    parse_md = models.BooleanField(default=False)
    next_block_number = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return f"{self.step}: {self.caption[:20]}"

# Options:
COLORS=[('yellow', 'Yellow'),('red', 'Red'),('green', 'Green'),('blue', 'Blue'),('none', 'None')]
class InteractiveOption(PolymorphicModel):
    question = models.ForeignKey(InteractiveQuestionBlock, related_name='options', on_delete=models.CASCADE)
    color = models.CharField(max_length=16, blank=True, choices=COLORS)
    next_block_number = models.PositiveIntegerField(null=True, blank=True)

class InteractiveTextOption(InteractiveOption):
    text = models.CharField(max_length=255)
    response= models.TextField(blank=True)
    parse_md_response=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.question}: {self.text}"
    
def step_option_image_upload_path(instance, filename):
    step_slug = instance.question.step.slug
    return f'steps/{step_slug}/images/{filename}'

class InteractiveImageOption(InteractiveOption):
    image = models.ImageField(upload_to=step_option_image_upload_path)
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    response= models.TextField(blank=True)
    parse_md_response=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.question}: {self.alt_text}"
