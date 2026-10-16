from django.db import models
import uuid
from django.core.exceptions import ValidationError

# Create your models here.
class TimeStampedUUIDModel (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class SchoolProfile(TimeStampedUUIDModel):
    name = models.CharField(max_length=255, default="Standard Academy")
    motto = models.CharField(max_length=255, blank=True,)
    logo = models.ImageField(upload_to='school_logos/logo/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)

    class Meta:
        verbose_name = "School Profile"
        verbose_name_plural = "School Profile"

    def save(self, *args, **kwargs):
        if not self.pk and SchoolProfile.objects.exists:
            raise ValidationError("Only one SchoolProfile instance is permitted.")
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(default={"name": "Standard Academy"})
        return obj

    def __str__(self):
        return self.name