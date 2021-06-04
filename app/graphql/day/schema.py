from app.schedule.models.daily_details import ActivityDetail
import graphene
import graphql_jwt
from graphene import relay
from django.contrib.auth import get_user_model
from ...schedule.models import Day, Note
from graphql_jwt.decorators import staff_member_required

from .types import AnonDayType, NoteType, DayUnion, ActivityDetailType
from .mutations import (
    CreateDay,
    CreateNote,
    CreateActivityDetail,
    EditNote,
    EditActivityDetail,
    DeleteNote,
)
from ..utils import get_viewer


User = get_user_model()


class DayQueries(graphene.ObjectType):
    day = graphene.Field(DayUnion, date=graphene.Date())
    notes = graphene.List(NoteType, date=graphene.Date())
    daily_activity_meta = graphene.List(ActivityDetailType, date=graphene.Date())
    activity_data = graphene.Field(ActivityDetailType, activity_id=graphene.ID())

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
        try:
            day = Day.objects.get(date=date)
            print(day)
            activities = ActivityDetail.objects.filter(day=day)
            print(activities)
            return activities
        except:
            return []

    def resolve_activity_data(self, info, activity_id):
        activity = ActivityDetail.objects.get(pk=activity_id)
        return activity


class DayMutations(graphene.ObjectType):
    create_day = CreateDay.Field()
    create_note = CreateNote.Field()
    edit_activity_detail = EditActivityDetail.Field()
    create_activity_detail = CreateActivityDetail.Field()
    edit_note = EditNote.Field()
    delete_note = DeleteNote.Field()
