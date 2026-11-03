from django.contrib import admin
from .models import StaffProfile
# Register your models here.
@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'user', 'qualification', 'date_joined', 'address')
    search_fields = ('staff_id', 'user__email', 'user__first_name', 'user__last_name')