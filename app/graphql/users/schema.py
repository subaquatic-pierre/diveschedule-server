import graphene
import graphql_jwt
from graphene import relay
from graphene_django import DjangoConnectionField
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import staff_member_required

from .types import UserType, UserConnection, ViewerResult, AnonUserType, ProfileType
from .mutations import CreateUser, EditUser, DeleteUser, EditProfile
from ..utils import get_viewer


User = get_user_model()


class UserQueries(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.ID())
    search_users = relay.ConnectionField(
        UserConnection, full_name=graphene.String(), required=False
    )
    all_users = relay.ConnectionField(UserConnection)
    viewer = graphene.Field(ViewerResult)
    profile = graphene.Field(ProfileType, username=graphene.String())

    def resolve_profile(self, info, username):
        user = User.objects.get(username=username)
        profile = user.profile
        return profile

    def resolve_search_users(self, info, full_name, **kwargs):
        return User.objects.filter(profile__full_name__icontains=full_name)

    # @staff_member_required
    def resolve_viewer(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            return AnonUserType(email="anon", is_staff=False)
        return get_viewer(info)

    # @staff_member_required
    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    # @staff_member_required
    def resolve_users(self, info, **kwargs):
        ids = kwargs.get("ids")
        user_list = []
        if ids:
            for id in ids:
                user = User.objects.get(id=id)
                user_list.append(user)

        return user_list

    # @staff_member_required
    def resolve_user(self, info, id):
        user = User.objects.get(id=id)

        return user


class UserMutations(graphene.ObjectType):
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    create_user = CreateUser.Field()
    edit_user = EditUser.Field()
    delete_user = DeleteUser.Field()
    edit_profile = EditProfile.Field()