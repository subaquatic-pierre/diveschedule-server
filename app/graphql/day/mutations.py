import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import staff_member_required

from ...schedule.models import Day, Note, TripDetail
from .types import NoteType, DayType, TripDetailType
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


class CreateTripDetail(graphene.Mutation):
    trip_detail = graphene.Field(TripDetailType)

    class Arguments:
        date = graphene.Date()
        trip_type = graphene.String()
        time = graphene.String(required=False)
        dive_site_1 = graphene.String(required=False)
        dive_site_2 = graphene.String(required=False)
        dive_guides = graphene.List(graphene.ID, required=False)

    def mutate(self, info, date, trip_type, **kwargs):
        day, created = Day.objects.get_or_create(date=date)
        time = kwargs.get("time")
        dive_site_1 = kwargs.get("dive_site_1")
        dive_site_2 = kwargs.get("dive_site_2")
        dive_guides = kwargs.get("dive_guides")
        trip_detail = TripDetail(day=day, trip_type=trip_type)
        trip_detail.save()

        if time:
            trip_detail.time = time
        if dive_site_1 != "":
            trip_detail.dive_site_1 = dive_site_1
        if dive_site_2 != "":
            trip_detail.dive_site_2 = dive_site_2

        if len(dive_guides) != 0:
            for id in dive_guides:
                guide = User.objects.get(pk=id)
                trip_detail.dive_guides.add(guide)

        trip_detail.save()

        return CreateTripDetail(trip_detail)


class EditTripDetail(graphene.Mutation):
    trip_detail = graphene.Field(TripDetailType)

    class Arguments:
        id = graphene.ID()
        dive_site_1 = graphene.String(required=False)
        dive_site_2 = graphene.String(required=False)
        dive_guides = graphene.List(graphene.ID, required=False)

    def mutate(self, info, id, **kwargs):
        trip_detail = TripDetail.objects.get(pk=id)

        dive_guides = kwargs.get("dive_guides")
        dive_site_1 = kwargs.get("dive_site_1")
        dive_site_2 = kwargs.get("dive_site_2")

        if dive_site_1:
            trip_detail.dive_site_1 = dive_site_1
        if dive_site_2:
            trip_detail.dive_site_2 = dive_site_2

        trip_detail.dive_guides.clear()

        if len(dive_guides) != 0:
            for id in dive_guides:
                guide = User.objects.get(pk=id)
                trip_detail.dive_guides.add(guide)

        trip_detail.save()

        return EditTripDetail(trip_detail)


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
