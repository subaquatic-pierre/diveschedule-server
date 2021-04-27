from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from graphql_jwt.decorators import jwt_cookie
from django.views.decorators.csrf import csrf_exempt
from .graphql.schema import schema


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path(
        "graphql/",
        csrf_exempt(jwt_cookie(GraphQLView.as_view(schema=schema, graphiql=True))),
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
