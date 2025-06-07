from django.contrib import admin
from .models import *

class RecordInline(admin.TabularInline):
    model = Record
    extra= 1

class RecomInline(admin.TabularInline):
    model = Recommendation
    extra= 1

class PatientAdmin(admin.ModelAdmin):
    inlines = [RecomInline, RecordInline]

# Register your models here.
admin.site.register(Record)
admin.site.register(Recommendation)
admin.site.register(Doctor)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Company)
