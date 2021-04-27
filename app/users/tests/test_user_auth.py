import json
from django.test import TestCase
from ...graphql.schema import schema
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from .utils import assert_no_errors

USER_EMAIL = "user@user.com"
USER_PASSWORD = "password"


class TestUserAuth(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(email=USER_EMAIL)
        self.user.set_password(USER_PASSWORD)
        self.user.save()
        self.client.login(username=USER_EMAIL, password=USER_PASSWORD)

    def test_user_login(self):
        """ Login user with email and password """
        query = """
            mutation UserLogin($email: String!, $password: String!) {
                tokenAuth(email: $email, password: $password) {
                    token
                }
            }
            """

        variables = {"email": USER_EMAIL, "password": USER_PASSWORD}
        response = self.client.execute(query, variables)
        assert_no_errors(response)
        assert "token" in response.data.get(
            "tokenAuth"
        ), "Failed to get token for user login"

    def test_get_viewer(self):
        """ Get Anonymous viewer """
        query = """
            query Viewer {
                viewer{
                    __typename
                    ... on UserType {
                        id
                    }
                }
            }
            """

        response = self.client.execute(query)
        assert_no_errors(response)
