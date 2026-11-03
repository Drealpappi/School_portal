from django.db import models
from django.conf import settings
from core.models import TimeStampedUUIDModel

# Create your models here.
class Student(TimeStampedUUIDModel):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    admission_number = models.CharField(max_length=100, unique=True, db_index=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices)
    address = models.TextField(blank=True)
    admission_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['admission_number']
    def __str__(self):
        return f"{self.user.full_name} ({self.admission_number})"

class Parent(TimeStampedUUIDModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='parent_profile'
    )

    address = models.TextField(blank=True)
    Students = models.ManyToManyField(Student, related_name='guradians', blank=True)

    def __str__(self):
        return f"Parent: {self.user.full_name}"

class Enrollment(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        PROMOTED = 'PROMOTED', 'Promoted'
        REPEATED = 'REPEATED', 'Repeated'
        GRADUATED = 'GRADUATED', 'Graduated'
        WITHDRAWN = 'WITHDRAWN', 'Withdrawn'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    class_room = models.ForeignKey('academics.ClassRoom', on_delete=models.PROTECT, related_name='enrollments')
    session = models.ForeignKey('academics.AcademicSession', on_delete=models.PROTECT, related_name='enrollments')
    status = models.CharField(max_length=80, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'session'],
                name='unique_student_enrollment_per_session'
            )
        ]
        ordering = ['-session__start_date', 'student__admission_number']

    def __str__(self):
        return f"{self.student.admission_number} -> {self.class_room} ({self.session.name})"