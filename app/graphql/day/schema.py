import graphene
import graphql_jwt
from graphene import relay
from django.contrib.auth import get_user_model
from ...schedule.models import Day, Note
from graphql_jwt.decorators import staff_member_required

from .types import AnonDayType, NoteType, DayUnion, TripDetailType
from .mutations import (
    CreateDay,
    CreateNote,
    CreateTripDetail,
    EditNote,
    EditTripDetail,
    DeleteNote,
)
from ..utils import get_viewer


User = get_user_model()


class DayQueries(graphene.ObjectType):
    day = graphene.Field(DayUnion, date=graphene.Date())
    notes = graphene.List(NoteType, date=graphene.Date())
    daily_activity_meta = graphene.List(TripDetailType, date=graphene.Date())

    def resolve_day(self, info, date):
        try:
            day = Day.objects.get(date=date)
            return day
        except:
            return AnonDayType(date=date)

    def resolve_notes(self, info, date):
        try:
            day = Day.objects.get(date=date)
            notes = Note.objects.filter(day=day)
            return notes
        except:
            return []

    def resolve_daily_activity_meta(self, info, date):
        day = Day.objects.get(date=date)
        print(day)
        return []


class DayMutations(graphene.ObjectType):
    create_day = CreateDay.Field()
    create_note = CreateNote.Field()
    create_trip_detail = CreateTripDetail.Field()
    edit_note = EditNote.Field()
    edit_trip_detail = EditTripDetail.Field()
    delete_note = DeleteNote.Field()
