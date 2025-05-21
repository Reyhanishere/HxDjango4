from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from polymorphic.models import PolymorphicModel



# === STEP & BLOCK SYSTEM ===
class Field(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title

class Step(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    field=models.ForeignKey(Field, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Block(PolymorphicModel):
    step = models.ForeignKey('Step', related_name='blocks', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ('step', 'order')

    def __str__(self):
        return f"{self.step.title} - Block {self.order}"

# === BLOCK TYPES ===

class TextBlock(Block):
    visible = models.BooleanField(default=True)
    text = models.TextField()

    def __str__(self):
        return f"{self.text[:50]}"


class ImageBlock(Block):
    visible = models.BooleanField(default=True)
    image = models.ImageField(upload_to='steps/images/')
    caption =  models.TextField(blank=True)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True)
    submitted_data = models.JSONField()  # Can store selected option, typed keywords, pairs, etc.
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user} to Block {self.block.id if self.block else 'Deleted Block'}"


class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True)
    completed_blocks = models.ManyToManyField(Block, blank=True)
    xp = models.IntegerField(default=10)
    streak = models.IntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} progress in {self.step}"

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
    
class Record(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='records')
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    
    class Meta:
        unique_together = ('race', 'name')

    def __str__(self):
        return f"{self.race}| {self.name}: {self.score}"
