from django.db import models
from django.conf import settings


CERT_LEVEL_CHOICES = [
    ("OW", "Open Water"),
    ("AOW", "Advanced Open Water"),
    ("RD", "Rescue Diver"),
    ("DEEP", "Deep Diver"),
    ("TEC50", "Technical 50m"),
    ("TRIMIX90", "Trimix 90m"),
    ("DM", "Divemaster"),
    ("INST", "Instructor"),
]

EQUIPMENT_CHOICES = [
    ("FK", "Full Kit"),
    ("TW", "Tanks and Weights"),
    ("NO", "No Equipment"),
]


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_name = models.CharField(
        max_length=256, default="Default Name", null=True, blank=True
    )

    email = models.EmailField(max_length=255, blank=True, null=True)

    cert_level = models.CharField(
        max_length=256,
        choices=CERT_LEVEL_CHOICES,
        default="OW",
        blank=True,
        null=True,
    )

    equipment = models.CharField(
        max_length=256,
        choices=EQUIPMENT_CHOICES,
        default="FK",
        blank=True,
        null=True,
    )
