import graphene
from graphene import relay, Union, ObjectType
from graphene_django import DjangoObjectType
from ...schedule.models import Day, Note, TripDetail


class DayType(DjangoObjectType):
    class Meta:
        model = Day


class TripDetailType(DjangoObjectType):
    class Meta:
        model = TripDetail


class AnonDayType(ObjectType):
    date = graphene.Date()


class DayUnion(Union):
    class Meta:
        types = (DayType, AnonDayType)


class NoteType(DjangoObjectType):
    class Meta:
        model = Note
