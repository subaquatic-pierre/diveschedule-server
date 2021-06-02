from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

DIVE_SITE_CHOICES = (
    ("Arificial Reef", "Arificial Reef"),
    ("Dibba Rock", "Dibba Rock"),
    ("Cauliflower Reef", "Cauliflower Reef"),
    ("The Nursery", "The Nursery"),
    ("Inchcape 1", "Inchcape 1"),
    ("Inchcape Deep", "Inchcape Deep"),
    ("Snoopy Island", "Snoopy Island"),
    ("Snoopy Deep", "Snoopy Deep"),
    ("Deep Sand", "Deep Sand"),
    ("Snoopy 50", "Snoopy 50"),
    ("3 Rocks", "3 Rocks"),
    ("Car Cemetary", "Car Cemetary"),
    ("Shark Island", "Shark Island"),
    ("Coral Gardens", "Coral Gardens"),
    ("Hole in the Wall", "Hole in the Wall"),
    ("Inchcape 2", "Inchcape 2"),
    ("Martini Rock", "Martini Rock"),
    ("Other", "Other"),
)

ACTIVITY_TYPE_CHOICES = (
    ("AM_BOAT", "AM_BOAT"),
    ("PM_BOAT", "PM_BOAT"),
    ("POOL", "POOL"),
    ("SHORE", "SHORE"),
    ("CLASS", "CLASS"),
)


class Day(models.Model):
    date = models.DateField()
    team_members_off = models.ManyToManyField(to=User)


class Note(models.Model):
    day = models.ForeignKey(to=Day, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __repr__(self):
        return f"Note(day={self.day},title={self.title},text={self.text}"


class ActivityDetail(models.Model):
    day = models.ForeignKey(to=Day, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255, choices=ACTIVITY_TYPE_CHOICES)
    time = models.CharField(max_length=255, null=True, blank=True)
    dive_site_1 = models.CharField(max_length=255, null=True, blank=True)
    dive_site_2 = models.CharField(max_length=255, null=True, blank=True)
    dive_guides = models.ManyToManyField(to=User)

    def __repr__(self):
        return f"ActivityDetail(day={self.day.date})"

    def __str__(self):
        return f"ActivityDetail(day={self.day.date}, trip_type={self.trip_type})"
