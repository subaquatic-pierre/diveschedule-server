from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from .daily_details import TripDetail

User = get_user_model()

# from django.contrib.auth import get_user_model


TRIP_TYPE_CHOICES = (
    ("AM_BOAT", "AM_BOAT"),
    ("PM_BOAT", "PM_BOAT"),
    ("POOL", "POOL"),
    ("SHORE", "SHORE"),
    ("CLASS", "CLASS"),
)
BOOKING_STATUS_CHOICES = (
    ("REQUESTED", "REQUESTED"),
    ("COMPLETED", "COMPLETED"),
    ("PENDING_CHANGE", "PEDNING_CHANGE"),
    ("CANCELLED", "CANCELLED"),
)

# default_user = get_user_model().objects.get(email="default@default.com")


class Booking(models.Model):
    trip_detail = models.ForeignKey(
        TripDetail, on_delete=models.SET_NULL, null=True, blank=True
    )
    time = models.CharField(max_length=255, null=True, blank=True)
    initiated_date = models.DateField(auto_now_add=True)
    diver = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    booked_by = models.ForeignKey(
        User,
        related_name="booked_by",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    activity = models.CharField(max_length=255, default="null")
    equipment = models.CharField(max_length=255, default="null")
    booking_status = models.CharField(
        max_length=255, choices=BOOKING_STATUS_CHOICES, blank=True, null=True
    )
    instructor = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="booking_instructor",
        null=True,
        blank=True,
    )
    cancellation_reason = models.CharField(max_length=256, blank=True, null=True)
