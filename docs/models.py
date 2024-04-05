from django.db import models

class Doc(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(null=False, blank=False)
    visible = models.BooleanField("Visibility",default=True ,null=False, blank=False)

    def __str__(self):
        return self.title
