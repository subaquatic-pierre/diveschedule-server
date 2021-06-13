import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import staff_member_required

from ...schedule.models import Day, Note, ActivityDetail
from .types import NoteType, DayType, ActivityDetailType
from ..utils import staff_permission_required


User = get_user_model()


class CreateDay(graphene.Mutation):
    day = graphene.Field(DayType)

    class Arguments:
        date = graphene.Date()

    # @staff_member_required
    def mutate(self, info, date):
        day, created = Day.objects.get_or_create(date=date)

        return CreateDay(day)


class CreateActivityDetail(graphene.Mutation):
    activity_detail = graphene.Field(ActivityDetailType)

    class Arguments:
        date = graphene.Date()
        activity_type = graphene.String()
        time = graphene.String(required=False)
        dive_site_1 = graphene.String(required=False)
        dive_site_2 = graphene.String(required=False)
        dive_guides = graphene.List(graphene.ID, required=False)

    def mutate(self, info, **kwargs):
        date = kwargs.get("date")
        day, created = Day.objects.get_or_create(date=date)
        time = kwargs.get("time")
        dive_site_1 = kwargs.get("dive_site_1")
        dive_site_2 = kwargs.get("dive_site_2")
        dive_guides = kwargs.get("dive_guides")
        activity_type = kwargs.get("activity_type")
        activity_detail = ActivityDetail(day=day, activity_type=activity_type)
        activity_detail.save()

        if time:
            activity_detail.time = time
        if dive_site_1 != "":
            activity_detail.dive_site_1 = dive_site_1
        if dive_site_2 != "":
            activity_detail.dive_site_2 = dive_site_2

        if len(dive_guides) != 0:
            for id in dive_guides:
                guide = User.objects.get(pk=id)
                activity_detail.dive_guides.add(guide)

        day.save()
        activity_detail.save()

        return CreateActivityDetail(activity_detail)


class EditActivityDetail(graphene.Mutation):
    activity_detail = graphene.Field(ActivityDetailType)

    class Arguments:
        id = graphene.ID()
        dive_site_1 = graphene.String(required=False)
        dive_site_2 = graphene.String(required=False)
        dive_guides = graphene.List(graphene.ID, required=False)

    def mutate(self, info, id, **kwargs):
        activity_detail = ActivityDetail.objects.get(pk=id)

        dive_guides = kwargs.get("dive_guides")
        dive_site_1 = kwargs.get("dive_site_1")
        dive_site_2 = kwargs.get("dive_site_2")

        if dive_site_1:
            activity_detail.dive_site_1 = dive_site_1
        if dive_site_2:
            activity_detail.dive_site_2 = dive_site_2

        activity_detail.dive_guides.clear()

        if len(dive_guides) != 0:
            for id in dive_guides:
                guide = User.objects.get(pk=id)
                activity_detail.dive_guides.add(guide)

        activity_detail.save()

        return EditActivityDetail(activity_detail)


class CreateNote(graphene.Mutation):
    note = graphene.Field(NoteType)

    class Arguments:
        date = graphene.Date()
        title = graphene.String()
        text = graphene.String()

    # @staff_member_required
    def mutate(self, info, date, title, text):
        day, created = Day.objects.get_or_create(date=date)
        note = Note.objects.create(day=day, title=title, text=text)
        note.save()

        return CreateNote(note)


class EditNote(graphene.Mutation):
    note = graphene.Field(NoteType)

    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=False)
        text = graphene.String(required=False)

    # @staff_member_required
    def mutate(self, info, id, title, text):
        note = Note.objects.get(pk=id)
        if title:
            note.title = title
        if text:
            note.text = text
        note.save()

        return EditNote(note)


class DeleteNote(graphene.Mutation):
    note = graphene.Field(graphene.Boolean)

    class Argumments:
        id = graphene.ID()

    def mutate(self, info, id):
        note = Note.objects.get(pk=id)
        note.delete()

        return DeleteNote(True)
