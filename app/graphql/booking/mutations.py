import graphene
from copy import copy
from django.core.exceptions import ObjectDoesNotExist

from .types import BookingType
from ..utils import get_viewer
from graphql_jwt.decorators import staff_member_required
from django.contrib.auth import get_user_model

from ...users.models import Profile
from ...schedule.models import Booking, Day, ActivityDetail

User = get_user_model()


class CreateBooking(graphene.Mutation):
    booking = graphene.Field(BookingType)

    class Arguments:
        user_id = graphene.ID(required=True)
        instructor_id = graphene.ID(required=False)
        date = graphene.Date(required=True)
        time = graphene.String(required=False)
        activity_type = graphene.String(required=True)
        diver_role = graphene.String(required=True)
        equipment = graphene.String(required=False)

    @staff_member_required
    def mutate(
        self, info, user_id, date, time, activity_type, diver_role, equipment, **kwargs
    ):
        instructor_id = kwargs.get("instructor_id")
        viewer = get_viewer(info)
        diver = User.objects.get(pk=user_id)

        day, created = Day.objects.get_or_create(date=date)
        activity_detail, created = ActivityDetail.objects.get_or_create(
            day=day, activity_type=activity_type
        )

        if not time:
            if activity_type == "AM_BOAT":
                activity_detail.time = "9AM"
            if activity_type == "PM_BOAT":
                activity_detail.time = "1:30PM"

        booking = Booking(
            time=time,
            activity_detail=activity_detail,
            diver=diver,
            diver_role=diver_role,
            equipment=equipment,
            booked_by=viewer,
        )

        try:
            instructor = User.objects.get(pk=instructor_id)
            booking.instructor = instructor
        except ObjectDoesNotExist:
            pass

        activity_detail.save()
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
        activity_type = graphene.String()
        full_name = graphene.String()
        diver_role = graphene.String()
        equipment = graphene.String()

    @staff_member_required
    def mutate(self, info, id, **kwargs):
        date = kwargs.get("date")
        time = kwargs.get("time")
        instructor_id = kwargs.get("instructor_id")
        activity_type = kwargs.get("activity_type")
        full_name = kwargs.get("full_name")
        diver_role = kwargs.get("diver_role")
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
        if activity_type:
            booking.activity_type = activity_type
        if full_name:
            booking.diver.profile.full_name = diver
        if diver_role:
            booking.diver_role = diver_role
        if equipment:
            booking.equipment = equipment

        booking.save()

        return EditBooking(booking=booking)


class DeleteBookings(graphene.Mutation):
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

        return DeleteBookings(bookings=booking_list)
