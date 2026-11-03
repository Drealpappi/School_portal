from django.contrib import admin
from .models import AcademicSession, Term, ClassLevel, ClassRoom, Subject, SubjectAllocation
# Register your models here.

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'session', 'start_date', 'end_date', 'is_current')
    list_filter = ('session', 'is_current')

@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'level_order')

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('level', 'arm', 'capacity', 'form_teacher')
    list_filter = ('level',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject_code', 'is_core')
    search_fields = ('name',)

@admin.register(SubjectAllocation)
class SubjectAllocationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'class_room', 'teacher', 'session')
    list_filter = ('session', 'class_room')