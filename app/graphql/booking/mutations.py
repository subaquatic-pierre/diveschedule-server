import graphene
from copy import copy
from django.core.exceptions import ObjectDoesNotExist

from .types import BookingType
from ..utils import get_viewer
from graphql_jwt.decorators import staff_member_required
from django.contrib.auth import get_user_model

from ...users.models import Profile
from ...schedule.models import Booking, Day, TripDetail

User = get_user_model()


class CreateBooking(graphene.Mutation):
    booking = graphene.Field(BookingType)

    class Arguments:
        user_id = graphene.ID(required=True)
        instructor_id = graphene.ID(required=False)
        date = graphene.Date(required=True)
        time = graphene.String(required=False)
        trip_type = graphene.String(required=True)
        activity = graphene.String(required=True)
        equipment = graphene.String(required=False)

    # @staff_member_required
    def mutate(
        self, info, user_id, date, time, trip_type, activity, equipment, **kwargs
    ):
        instructor_id = kwargs.get("instructor_id")
        viewer = get_viewer(info)
        diver = User.objects.get(pk=user_id)

        day, created = Day.objects.get_or_create(date=date)
        trip_detail, created = TripDetail.objects.get_or_create(
            day=day, trip_type=trip_type
        )

        if not time:
            if trip_type == "AM_BOAT":
                trip_detail.time = "9AM"
            if trip_type == "PM_BOAT":
                trip_detail.time = "1:30PM"

        booking = Booking(
            time=time,
            trip_detail=trip_detail,
            diver=diver,
            activity=activity,
            equipment=equipment,
            booked_by=viewer,
        )

        try:
            instructor = User.objects.get(pk=instructor_id)
            booking.instructor = instructor
        except ObjectDoesNotExist:
            pass

        trip_detail.save()
        day.save()
        booking.save()

        return CreateBooking(booking=booking)


class EditBooking(graphene.Mutation):
    booking = graphene.Field(BookingType)

    class Arguments:
        id = graphene.ID(required=True)
        instructor_id = graphene.ID(required=False)
        date = graphene.Date()
        time = graphene.String()
        trip_type = graphene.String()
        full_name = graphene.String()
        activity = graphene.String()
        equipment = graphene.String()

    @staff_member_required
    def mutate(self, info, id, **kwargs):
        date = kwargs.get("date")
        time = kwargs.get("time")
        instructor_id = kwargs.get("instructor_id")
        trip_type = kwargs.get("trip_type")
        full_name = kwargs.get("full_name")
        activity = kwargs.get("activity")
        equipment = kwargs.get("equipment")

        booking = Booking.objects.get(pk=id)
        diver, created = User.objects.get_or_create(username=full_name)

        if created:
            profile = Profile(user=diver)
            profile.save()

        if date:
            booking.date = date
        if time:
            booking.time = time
        if trip_type:
            booking.trip_type = trip_type
        if full_name:
            booking.diver.profile.full_name = diver
        if activity:
            booking.activity = activity
        if equipment:
            booking.equipment = equipment

        booking.save()

        return EditBooking(booking=booking)


class DeleteBooking(graphene.Mutation):
    bookings = graphene.List(BookingType)

    class Arguments:
        ids = graphene.List(graphene.ID, required=True)

    @staff_member_required
    def mutate(self, info, ids):
        booking_list = []
        for id in ids:
            booking = Booking.objects.get(id=id)
            booking_list.append(copy(booking))
            booking.delete()

        return DeleteBooking(bookings=booking_list)