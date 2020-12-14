from django.contrib import admin
from .models import VinNumber

# Register your models here.
admin.site.site_header = "VDA ADMINISTRATION"
admin.site.site_title = "fota"
admin.site.index_title = "Welcome to VDA Administration Portal"


admin.site.register(VinNumber)


