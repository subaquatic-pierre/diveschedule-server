import graphene
from graphene import relay, Union, ObjectType
from graphene_django import DjangoObjectType
from ...schedule.models import Day, Note, ActivityDetail


class DayType(DjangoObjectType):
    class Meta:
        model = Day


class ActivityDetailType(DjangoObjectType):
    class Meta:
        model = ActivityDetail


class AnonDayType(ObjectType):
    date = graphene.Date()


class DayUnion(Union):
    class Meta:
        types = (DayType, AnonDayType)


class NoteType(DjangoObjectType):
    class Meta:
        model = Note
