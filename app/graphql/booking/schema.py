from app.schedule.models.daily_details import ActivityDetail
import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import staff_member_required


from .types import BookingType
from .mutations import CreateBooking, EditBooking, DeleteBookings
from ..utils import staff_permission_required
from ...schedule.models import Booking

User = get_user_model()


class BookingQueries(graphene.ObjectType):
    booking = graphene.Field(
        BookingType, id=graphene.ID(), description="Get a single booking"
    )

    daily_bookings = graphene.List(
        BookingType,
        date=graphene.String(required=True),
        description="Get a list of bookings from a list of given ids, date or userId",
    )

    # @staff_member_required
    def resolve_daily_bookings(self, info, date):
        return Booking.objects.filter(date=date)

    @staff_member_required
    def resolve_booking(self, info, id):
        booking = Booking.objects.get(id=id)

        return booking


class BookingMutations(graphene.ObjectType):
    create_booking = CreateBooking.Field()
    edit_booking = EditBooking.Field()
    delete_bookings = DeleteBookings.Field()
