from django.db import models
from django.urls import reverse
from django.conf import settings

class CalCate(models.Model):
    title=models.CharField(max_length=64, null= False, blank= False)
    link = models.SlugField(max_length=64, unique= True ,null= False, blank= False)
    date_created= models.DateField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse("calcates_detail", kwargs={"link": self.link})
    
    def __str__(self):
        return str(self.title)

class Calculi(models.Model):
    html_title=models.CharField(max_length=63, null=False, blank= False)
    title=models.CharField(max_length=255, null=False, blank= False)
    category = models.ForeignKey(CalCate, null=False, blank= False, on_delete=models.CASCADE)
    link = models.SlugField(max_length=63, unique= True ,null= False, blank= False)
    html=models.CharField(max_length=31, null=False, blank= False)
    description=models.TextField(null=False, blank= False)
    date_created= models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CaLike',
        through_fields=('calculi', 'user'),
        related_name='liked_calculus'
    )
    like_count = models.PositiveIntegerField(default=0, db_index=True)  # Denormalized count
    
    class Meta:
        indexes = [
            models.Index(fields=['like_count']),
        ]

    def update_like_count(self):
        self.like_count = self.likes.count()
        self.save(update_fields=['like_count'])
    
    def get_absolute_url(self):
        return reverse("calculi_page", kwargs={"link": self.link})

    def __str__(self):
        return str(self.html_title) + " | " + str(self.category)
    
class CaLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    calculi = models.ForeignKey(Calculi, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user) + ": " + str(self.calculi)
    
    class Meta:
        unique_together = ('user', 'calculi')  # Prevent duplicate likes
        indexes = [
            models.Index(fields=['user', 'calculi']),  # user-specific queries
            models.Index(fields=['calculi', 'user']),  # calculator-specific queries
        ]

class CaLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    api_name = models.CharField(max_length=127)
    input_data = models.CharField(max_length=255, null=True, blank=True)
    output = models.CharField(max_length=255, null=True, blank=True)
    status = models.IntegerField()
    error_data = models.CharField(max_length=127, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    def __str__(self):
        try: 
            self.user.username
            return f"{self.user.username} | {self.api_name[9:]} {self.status}: {self.input_data} -> {self.output}"
        except:
            return f"Annonymus: {self.ip_address} | {self.api_name[9:]} {self.status}: {self.input_data} -> {self.output}"
