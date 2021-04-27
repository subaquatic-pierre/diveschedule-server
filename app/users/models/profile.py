from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    certification_level = models.CharField(
        max_length=256, default="Default", blank=True, null=True
    )
    equipment = models.CharField(
        max_length=256, default="Default", blank=True, null=True
    )
    full_name = models.CharField(
        max_length=256, default="Default", null=True, blank=True
    )
