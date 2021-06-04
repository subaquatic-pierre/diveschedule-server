import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import staff_member_required

from ...users.models import Profile
from .types import UserType

User = get_user_model()


class RegisterUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=False)
        cert_level = graphene.String(required=False)
        equipment = graphene.String(required=False)
        full_name = graphene.String(required=False)
        is_superuser = graphene.Boolean(required=False)
        is_staff = graphene.Boolean(required=False)

    def mutate(self, info, **kwargs):

        # User model fields
        password = kwargs.get("password", "password")
        email = kwargs.get("email")

        user = User(email=email, password=password)
        user.set_password(password)

        # Profile model fields
        full_name = kwargs.get("full_name")
        equipment = kwargs.get("equipment")
        cert_level = kwargs.get("cert_level")

        profile = Profile(user=user)
        profile.email = user.email
        if full_name:
            profile.full_name = full_name
        if equipment:
            profile.equipment = equipment
        if cert_level:
            profile.cert_level = cert_level

        user.save()
        profile.save()

        return RegisterUser(user=user)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=False)
        cert_level = graphene.String(required=False)
        equipment = graphene.String(required=False)
        full_name = graphene.String(required=False)
        phone_number = graphene.String(required=False)
        is_superuser = graphene.Boolean(required=False)
        is_staff = graphene.Boolean(required=False)

    @staff_member_required
    def mutate(self, info, **kwargs):
        # User model fields
        password = kwargs.get("password", "password")
        email = kwargs.get("email")

        user = User(email=email)
        user.set_password(password)

        # Profile model fields
        full_name = kwargs.get("full_name")
        equipment = kwargs.get("equipment")
        cert_level = kwargs.get("cert_level")
        phone_number = kwargs.get("phone_number")

        profile = Profile(user=user)
        profile.email = user.email
        if full_name:
            profile.full_name = full_name
        if equipment:
            profile.equipment = equipment
        if cert_level:
            profile.cert_level = cert_level
        if phone_number:
            profile.phone_number = phone_number

        user.save()
        profile.save()

        return CreateUser(user=user)


class UpdateProfile(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        userId = graphene.ID()
        email = graphene.String(required=False)
        password = graphene.String(required=False)
        full_name = graphene.String(required=False)
        phone_number = graphene.String(required=False)
        cert_level = graphene.String(required=False)
        equipment = graphene.String(required=False)
        is_superuser = graphene.Boolean(required=False)
        is_staff = graphene.Boolean(required=False)

    def mutate(self, info, userId, **kwargs):

        user = User.objects.get(pk=userId)
        profile = Profile.objects.get(user=user)

        # User model fields
        password = kwargs.get("password", "password")

        if password:
            user.set_password(password)

        # Profile model fields
        email = kwargs.get("email")
        full_name = kwargs.get("full_name")
        equipment = kwargs.get("equipment")
        cert_level = kwargs.get("cert_level")
        phone_number = kwargs.get("phone_number")

        profile.full_name = full_name
        profile.email = email

        if equipment:
            profile.equipment = equipment
        if cert_level:
            profile.cert_level = cert_level
        if phone_number:
            profile.phone_number = phone_number

        user.save()
        profile.save()

        return CreateUser(user=user)


class DeleteUsers(graphene.Mutation):
    deleted = graphene.Boolean()
    ids = graphene.List(graphene.ID)

    class Arguments:
        ids = graphene.List(graphene.ID, required=True)

    @staff_member_required
    def mutate(self, info, ids):
        for id in ids:
            user = User.objects.get(id=id)
            if not user:
                raise Exception("No user found")

            user.delete()

        return DeleteUsers(deleted=True, ids=ids)
