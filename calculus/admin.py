from django.contrib import admin
from .models import *

class CLAdmin(admin.ModelAdmin):
    list_display=["status", "api_name", "user"]

admin.site.register(Calculi)
admin.site.register(CalCate)
admin.site.register(CaLog, CLAdmin)
admin.site.register(CaLike)




