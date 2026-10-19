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
    class TermChoice(models.TextChoice):
        FIRST = 'FIRST', 'First Term'
        SECOND = 'SECOND', 'Second Term'
        THIRD = 'THIRD', 'Third Term'

    session = models.ForeignKey(AcademicSession, on_dete=models.CASCADE, related_name='terms')
    namee = models.CharField(max_length=25, choices=TermChoice.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BoleanField(default=False)

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
    level_order = models.PositiveSmallIntergerField(unique=True, help_text="e.g., It used for automatic promotion (1 for JSS 1, 2 for JSS 2)")

    class Meta:
        ordering = ['lever_oder']

    def __str__(self):
        return self.name