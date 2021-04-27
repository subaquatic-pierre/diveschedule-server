from graphene_django import DjangoObjectType
from graphene import relay
from ...schedule.models import Booking


class BookingType(DjangoObjectType):
    class Meta:
        model = Booking
        interface = (relay.Node,)


class BookingConnection(relay.Connection):
    class Meta:
        node = BookingType