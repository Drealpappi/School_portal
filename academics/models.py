from django.db import models, transaction
from core.models import TimeStampedUUIDModel
# Create your models here.

class AcademicSession(TimeStampedUUIDModel):
    name = models.CharField(max_length=25, unique=True, help_text="e.g., 2026/2027")
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_current:
                AcademicSession.objects.filter(is_current=True).exclude(pk=self.pk).update(is_current=False)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Term(TimeStampedUUIDModel):
    class TermChoice(models.TextChoices):
        FIRST = 'FIRST', 'First Term'
        SECOND = 'SECOND', 'Second Term'
        THIRD = 'THIRD', 'Third Term'

    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='terms')
    name = models.CharField(max_length=25, choices=TermChoice.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session', 'name'], name='unique_term_per_session')
        ]

        ordering = ['session', 'start_date', 'end_date']

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_current:
                Term.objects.filter(is_current=True).exclude(pk=self.pk).update(is_current=False)
            super().save(*args, **kwargs)
            

    def __str__(self):
        return f"{self.get_name_display()} ({self.session.name})"
    

class ClassLevel(TimeStampedUUIDModel):
    name = models.CharField(max_length=30, unique=True, help_text="e.g., JSS 1, JSS 2, JSS3, Nusery 1")
    level_order = models.PositiveSmallIntegerField(unique=True, help_text="e.g., It used for automatic promotion (1 for JSS 1, 2 for JSS 2)")

    class Meta:
        ordering = ['level_order']

    def __str__(self):
        return self.name


class ClassRoom(TimeStampedUUIDModel):
    level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name='classroom')
    arm = models.CharField(max_length=25, help_text="e.g., A, N1, P1, Science")
    capacity = models.PositiveSmallIntegerField(default=50)
    form_teacher = models.ForeignKey('staff.StaffProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='class_manager')

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['level', 'arm'], name='unique_level_arm')
        ]

        
        ordering = ['level__level_order', 'arm']

    def __str__(self):
        return f"{self.level.name} {self.arm}"

class Subject(TimeStampedUUIDModel):
    name = models.CharField(max_length=60, unique=True)
    subject_code = models.CharField(max_length=15, unique=True, help_text="e.g., MATH, PHE, ENG, PHY, CHM")
    is_core = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} {self.subject_code}"

class SubjectAllocation(TimeStampedUUIDModel):
    teacher = models.ForeignKey('staff.StaffProfile', on_delete=models.CASCADE, related_name='allocations')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='allocations')
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='subject_allocations')
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='subject_allocations')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subject', 'class_room', 'session'],
                                    
                name='unique_subject_classroom_session_allocation'
            )
        ]

    def __str__(self):
        return f"{self.subject_code} - {self.class_room} ({self.teacher.user.full_name})"