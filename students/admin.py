from django.contrib import admin
from .models import Student, Parent, Enrollment
# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'user', 'gender', 'date_of_birth', 'admission_date')
    search_fields = ('admission_number', 'user__first_name', 'user__last_name', 'user__email')
    list_filter = ('gender',)

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('Students',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_room', 'session', 'status')
    list_filter = ('session', 'class_room', 'status')
    search_fields = ('student__admission_number', 'student__user__first_name')