from django.db import models


class MedicalSubject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MedicalConcept(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=50, blank=True)
    subject = models.ManyToManyField(MedicalSubject)
    ai_used = models.BooleanField(default= False)

    def __str__(self):
        return self.name
        # if self.code:
        #     final+=" | "+self.code
        # return final
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Create a TermVariant with the same name as the concept
            TermVariant.objects.create(text=self.name.lower(), concept=self)


class TermVariant(models.Model):
    text = models.CharField(max_length=100, unique=True)
    concept = models.ForeignKey(
        MedicalConcept, on_delete=models.SET_NULL, related_name="variants", null=True
    )
    term_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.text} | {self.concept.name}"
    
    def save(self, *args, **kwargs):
        self.text = self.text.strip()
        super().save(*args, **kwargs)

class UnmappedTerm(models.Model):
    text = models.CharField(max_length=100, unique=True)
    score = models.SmallIntegerField(default=50)
    concept = models.ForeignKey(MedicalConcept, on_delete=models.CASCADE)
    matched_term = models.ForeignKey(TermVariant, on_delete=models.CASCADE, null=True)
    common_similarity=models.BooleanField(default=True, help_text='Is the Term Similar to One of Its Concept Variants?')
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    seen_count = models.IntegerField(default=1)

    def __str__(self):
        matched_term = 'No Matched Term'
        if self.matched_term:
            matched_term = self.matched_term.text
        return f"{self.text} ({self.score}%) - {matched_term} | {self.concept}"


