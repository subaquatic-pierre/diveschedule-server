from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from ...graphql.schema import schema
from django.contrib.auth import get_user_model
from ...users.models import Profile

from .utils import parse_response

User = get_user_model()


class TestUser(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self) -> None:
        first_user = User.objects.create(email="test@test.com")
        first_user.set_password("password")
        first_user.save()
        profile = Profile.objects.create(user=first_user)
        profile.full_name = "Test User"
        profile.save()

        return super().setUp()

    def test_create_user(self):
        """ Create user mutation """
        response = self.query(
            """
            mutation CreateUser($email: String, $password: String) {
                createUser(email: $email, password: $password){
                    user {
                        id
                    }
                }
            }
             """,
            op_name="CreateUser",
            variables={"email": "user@user.com", "password": "password"},
        )
        self.assertResponseNoErrors(response)
        data = parse_response(response)

        assert "id" in data.get("createUser").get("user")

    def test_edit_user(self):
        """ Edit user mutation """
        response = self.query(
            """
            mutation EditUser(
                $id: ID!
                $fullName: String
                $email: String
                $certificationLevel: String
                $equipment: String
            ) {
                editUser(
                id: $id
                fullName: $fullName
                email: $email
                certificationLevel: $certificationLevel
                equipment: $equipment
                ) {
                    user {
                        email
                        profile {
                            fullName
                            certificationLevel
                            equipment
                        }
                    }
                }
            }
             """,
            op_name="EditUser",
            variables={
                "id": 1,
                "fullName": "Peter Lemon",
                "email": "peter@lemon.com",
                "certificationLevel": "OW",
                "equipment": "FK",
            },
        )
        self.assertResponseNoErrors(response)
        data = parse_response(response)

        user_data = data.get("editUser").get("user")
        profile = user_data.get("profile")

        assert (
            user_data["email"] == "peter@lemon.com"
        ), f"Incorrect mutation response {user_data}"
        assert (
            profile["fullName"] == "Peter Lemon"
        ), f"Incorrect mutation response {profile}"
        assert (
            profile["certificationLevel"] == "OW"
        ), f"Incorrect mutation response {profile}"
        assert profile["equipment"] == "FK", f"Incorrect mutation response {profile}"

    def test_get_single_user(self):
        """ Get a single user by ID """
        response = self.query(
            """
            query GetUser($id: ID!) {
                user(id: $id) {
                    id
                }
            }""",
            op_name="GetUser",
            variables={
                "id": 1,
            },
        )
        self.assertResponseNoErrors(response)

        data = parse_response(response)
        user_data = data.get("user")
        assert (
            user_data["id"] == "1"
        ), f"Incorrect user returned from query, {user_data}"

    def test_get_all_users(self):
        """ Get all users """
        response = self.query(
            """
            query GetUser {
                allUsers{
                    edges {
                        node {
                            id
                        }
                    }
                }
            }""",
            op_name="GetUser",
        )
        self.assertResponseNoErrors(response)

        data = parse_response(response)
        all_users = data.get("allUsers").get("edges")
        assert len(all_users) >= 1, f"No users found, {all_users}"

    def test_search_users(self):
        response = self.query(
            """ 
            query SearchUsers($fullName: String!) {
                searchUsers(fullName: $fullName, first: 6) {
                    edges {
                        node {
                            id
                            profile {
                                fullName
                                certificationLevel
                                equipment
                            }
                        }
                    }
                }
            }
             """,
            op_name="SearchUsers",
            variables={"fullName": "Te"},
        )
        self.assertResponseNoErrors(response)

        data = parse_response(response)
        users = data.get("searchUsers").get("edges")
        assert len(users) >= 1, f"No users found, {data}"
        user = users[0].get("node")
        assert (
            user.get("profile").get("fullName") == "Test User"
        ), f"Incorrect user found, {user}"

    def test_delete_user(self):
        response = self.query(
            """ 
            mutation DeleteUser($ids: [ID]!) {
                deleteUser(ids: $ids) {
                    deleted
                    ids
                }
            }
             """,
            op_name="DeleteUser",
            variables={"ids": [1]},
        )
        self.assertResponseNoErrors(response)

        data = parse_response(response)
        assert (
            data.get("deleteUser").get("deleted") == True
        ), f"User was not deleted, {data}"
        assert data.get("deleteUser").get("ids") == [
            "1"
        ], f"Incorrect user deleted, {data}"