from django.db import models
from django.conf import settings
from core.models import TimeStampedUUIDModel

# Create your models here.
class StaffProfile(TimeStampedUUIDModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    staff_id = models.CharField(max_length=20, unique=True, db_index=True)
    qualification = models.CharField(max_length=80, blank=True, help_text="e.g., B.Sc Ed, B.Sc PEd, M.Sc")
    date_joined = models.DateField()
    address = models.TextField(blank=True)

    class Meta:
        ordering = ['staff_id']

    def __str__(self):
        return f"{self.user.full_name} ({self.staff_id})"

