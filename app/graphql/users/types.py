import graphene
from graphene_django import DjangoObjectType
from graphene import relay, Union, ObjectType
from django.contrib.auth import get_user_model
from ...users.models import Profile

User = get_user_model()


class AnonUserType(ObjectType):
    email = graphene.String()
    is_admin = graphene.Boolean()

    class Meta:
        interface = (relay.Node,)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            "full_name": ["exact", "icontains", "istartswith"],
            "email": ["exact", "icontains", "istartswith"],
        }
        interface = (relay.Node,)


class ViewerResult(Union):
    class Meta:
        types = (AnonUserType, UserType)


class UserConnection(relay.Connection):
    class Meta:
        node = UserType


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        interface = (relay.Node,)


class ProfileConnection(relay.Connection):
    class Meta:
        node = ProfileType
