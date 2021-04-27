from .users.schema import UserQueries, UserMutations
from .booking.schema import BookingQueries, BookingMutations
from .day.schema import DayQueries, DayMutations
import graphql_jwt


import graphene


class RootMutation(
    UserMutations,
    BookingMutations,
    DayMutations,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


class RootQuery(UserQueries, BookingQueries, DayQueries, graphene.ObjectType):
    pass


schema = graphene.Schema(query=RootQuery, mutation=RootMutation)