from django.db import models
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False)
    slug = models.SlugField(null=False, blank=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(null=False, blank=False)
    date = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    is_md = models.BooleanField(("MarkDown Active"),default=True ,null=False, blank=False)
    visible = models.BooleanField("Visibility",default=True ,null=False, blank=False)

    def __str__(self):
        return self.title
