from graphene_django.utils.testing import GraphQLTestCase
from ...graphql.schema import schema
from django.contrib.auth import get_user_model


from .utils import parse_response, print_data

User = get_user_model()


class TestTripDetail(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ["users", "profiles", "days", "bookings"]

    def setUp(self) -> None:
        self.client.defaults["Authorization"] = f"JWT {self.get_token()}"
        return super().setUp()

    def get_token(self):
        response = self.query(
            """ 
            mutation GetToken($email: String!, $password: String!){
                tokenAuth(email: $email, password: $password) {
                    token
                }
            }
            """,
            op_name="GetToken",
            variables={"email": "pierre@divesandybeach.com", "password": "password"},
        )
        data = parse_response(response)
        token = data.get("tokenAuth").get("token")
        return token

    def test_create_booking(self):
        """ Create booking mutation """
        response = self.query(
            """
            mutation CreateBooking(
                $activity: String!
                $userId: ID!
                $tripType: String!
                $date: Date!
                $equipment: String!
                $time: String!
                $instructorId: ID
            ) {
                createBooking(
                activity: $activity
                userId: $userId
                tripType: $tripType
                date: $date
                equipment: $equipment
                time: $time
                instructorId: $instructorId
                ) {
                    booking {
                        ...BookingFragment
                    }
                }
            }
            fragment BookingFragment on BookingType {
                id
                activity
                equipment
                time
                tripDetail {
                    tripType
                }
                instructor {
                    ...ProfileFragment
                }
                diver {
                    ...ProfileFragment
                }
            }
            fragment ProfileFragment on UserType {
                profile {
                    fullName
                    certificationLevel
                }
            }
            """,
            op_name="CreateBooking",
            variables={
                "activity": "PD",
                "userId": 3,
                "tripType": "AM_BOAT",
                "date": "2021-03-30",
                "equipment": "FK",
                "time": "9AM",
            },
        )
        data = parse_response(response)
        self.assertResponseNoErrors(response)

        booking = data.get("createBooking").get("booking")

        assert "id" in booking
        assert "diver" in booking
        assert "activity" in booking
        assert "equipment" in booking
        assert "tripDetail" in booking

    def test_get_booking(self):
        """ Get a booking """
        response = self.query(
            """
            query GetBooking($id: ID!) {
                booking(id: $id) {
                    id
                }
            }""",
            op_name="GetBooking",
            variables={
                "id": 1,
            },
        )
        self.assertResponseNoErrors(response)

    def test_delete_booking(self):
        """ Delete a booking """
        response = self.query(
            """
            mutation DeleteBooking($ids: [ID]!) {
                deleteBooking(ids: $ids){
                    bookings {
                        id
                    }
                }
            }""",
            op_name="DeleteBooking",
            variables={"ids": [1, 2, 3]},
        )
        self.assertResponseNoErrors(response)
