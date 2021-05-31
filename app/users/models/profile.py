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
    class CertLevelChoices(models.TextChoices):
        OW = "OW", _("Open Water")
        AOW = "AOW", _("Advanced Open Water")
        RD = "RD", _("Rescue Diver")
        DEEP = "DEEP", _("Deep Diver")
        TEC50 = "TEC50", _("Technical 50m")
        TRIMIX90 = "TRIMIX90", _("Trimix 90m")
        DM = "DM", _("Divemaster")
        INST = "INST", _("Instructor")

    class EquipmentChoices(models.TextChoices):
        FK = "FK", _("Full Kit")
        TW = "TW", _("Tanks and Weights")
        NO = "NO", _("No Equipment")

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_name = models.CharField(
        max_length=256, default="Default", null=True, blank=True
    )

    email = models.EmailField(
        max_length=255, default="default@email.com", blank=True, null=True
    )

    cert_level = models.CharField(
        max_length=256,
        choices=CertLevelChoices.choices,
        default=CertLevelChoices.OW,
        blank=True,
        null=True,
    )

    equipment = models.CharField(
        max_length=256,
        choices=EquipmentChoices.choices,
        default=EquipmentChoices.FK,
        blank=True,
        null=True,
    )
