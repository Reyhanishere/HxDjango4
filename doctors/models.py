from django.db import models
from django.conf import settings
from django.utils import timezone


class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    website=models.URLField(null=True, blank=True)
    expiration_date=models.DateField(editable=True, null=True)
    def __str__(self):
        return self.user.username

class Doctor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=100,
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.user.username} | {self.company.user.username}"

class Patient(models.Model):
    name = models.CharField(("نام"), max_length=100, null=False, blank=False)
    personal_id=models.SlugField(("کد ملی یا شمارۀ گذرنامه"), max_length=10, unique=True, null=False, blank=False)
    gender = models.CharField(
        ("جنسیت"),
        max_length=5,
        choices=[("پسر", "پسر"), ("دختر", "دختر")],
        null=False,
        blank=False,
        default='پسر'
    )
    # birth_date=models.DateField(editable=True, null=True)
    birth_date=models.DateField(editable=True, null=True)

    def __str__(self):
        return self.name
    
class Record(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    
    weight = models.FloatField(('Weight Value'), null=False, blank=False, default=0)
    weight_z = models.FloatField(('Weight Z Score'), null=False, blank=False, default=0)
    weight_p = models.FloatField(('Weight Percentile'), null=False, blank=False, default=0)
    height = models.SmallIntegerField(('Height Value'), null=False, blank=False, default=0)
    height_z = models.FloatField(('Height Z Score'), null=False, blank=False, default=0)
    height_p = models.FloatField(('Height Percentile'), null=False, blank=False, default=0)
    bmi = models.FloatField(('BMI Value'), null=False, blank=False, default=0)
    bmi_z = models.FloatField(('BMI Z Score'), null=False, blank=False, default=0)
    bmi_p = models.FloatField(('BMI Percentile'), null=False, blank=False, default=0)
    hc = models.FloatField(('Head Circumference Value'), null=True, blank=True, default=0)
    hc_z = models.FloatField(('Head Circumference Z Score'), null=True, blank=True, default=0)
    hc_p = models.FloatField(('Head Circumference Percentile'), null=True, blank=True, default=0)

    gender = models.CharField(max_length=5, null=False, blank=True)
    age_months = models.FloatField(('Age in monthes'), null=False, blank=False, default=0)

    record_add_date=models.DateTimeField(editable=True,)
    record_edit_date=models.DateTimeField(auto_now=True, editable=True, blank=True, null=True)

    def save(self, *args, **kwargs):
            if not self.id:
                self.record_add_date = timezone.now()
            super().save(*args, **kwargs)

    def __str__(self):
        return self.patient.name
