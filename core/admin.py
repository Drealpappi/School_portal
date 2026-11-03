from django.contrib import admin
from .models import SchoolProfile

# Register your models here.
@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    