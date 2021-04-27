import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import staff_member_required

from ...users.models import Profile
from .types import UserType
from ..utils import staff_permission_required
from .types import ProfileType


User = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        password = graphene.String(required=False)
        email = graphene.String(required=False)
        certification_level = graphene.String(required=False)
        equipment = graphene.String(required=False)
        full_name = graphene.String(required=False)

    # @staff_member_required
    def mutate(self, info, *args, **kwargs):
        dummy_email = f"default_email_{len(User.objects.all())+1}@default.com"

        password = kwargs.get("password", "password")
        email = kwargs.get("email", dummy_email)
        full_name = kwargs.get("full_name", "default")
        equipment = kwargs.get("equipment", "default")
        certification_level = kwargs.get("certification_level", "default")

        user = User(
            email=email,
        )
        user.set_password(password)

        profile = Profile(user=user)
        profile.full_name = full_name
        profile.equipment = equipment
        profile.certification_level = certification_level

        user.save()
        profile.save()

        return CreateUser(user=user)


class EditUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)
        password = graphene.String(required=False)
        email = graphene.String(required=False)
        certification_level = graphene.String(required=False)
        equipment = graphene.String(required=False)
        full_name = graphene.String(required=False)

    # @staff_member_required
    def mutate(self, info, **kwargs):
        id = kwargs.get("id")
        password = kwargs.get("password")
        email = kwargs.get("email")
        full_name = kwargs.get("full_name")
        equipment = kwargs.get("equipment")
        certification_level = kwargs.get("certification_level")

        user = User.objects.get(id=id)
        profile = Profile.objects.get(user=user)

        if not user:
            raise Exception("No user found")

        if password:
            user.set_password(password)
        if email:
            user.email = email
        if certification_level:
            profile.certification_level = certification_level
        if full_name:
            profile.full_name = full_name
        if equipment:
            profile.equipment = equipment

        profile.save()
        user.save()

        return EditUser(user=user)


class DeleteUser(graphene.Mutation):
    deleted = graphene.Boolean()
    ids = graphene.List(graphene.ID)

    class Arguments:
        ids = graphene.List(graphene.ID, required=True)

    # @staff_member_required
    def mutate(self, info, ids):
        for id in ids:
            user = User.objects.get(id=id)

            if not user:
                raise Exception("No user found")

            user.delete()

        return DeleteUser(deleted=True, ids=ids)


class EditProfile(graphene.Mutation):
    profile = graphene.Field(ProfileType)

    class Arguments:
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @staff_member_required
    def mutate(self, info, password, email):
        profile = User.objects.get(id=1).profile
        return profile