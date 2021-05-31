from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from ...graphql.schema import schema
from django.contrib.auth import get_user_model
from ...users.models import Profile
from ...schedule.models import Day, Note, TripDetail

from .utils import parse_response, print_data

User = get_user_model()


class TestDay(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ["users", "profiles", "days", "bookings"]

    def setUp(self) -> None:

        return super().setUp()

    def test_get_day(self):
        """Get a day"""
        response = self.query(
            """ 
            query GetDay($date: Date!) {
                day(date: $date) {
                    __typename
                    ... on DayType {
                        teamMembersOff {
                            ...ProfileFragment
                        }
                        noteSet {
                            title
                            text
                        }
                        tripdetailSet {
                            ...TripDetailFragment
                            bookingSet {
                            ...BookingFragment
                            }
                        }
                    }
                }
            }

            fragment BookingFragment on BookingType {
                id
                activity
                equipment
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
                    certLevel
                }
            }   

            fragment TripDetailFragment on TripDetailType {
                tripType
                diveSite1
                diveSite2
                diveGuides {
                    ...ProfileFragment
                }
            }

            """,
            op_name="GetDay",
            variables={"date": "2021-03-30"},
        )
        self.assertResponseNoErrors(response)
        data = parse_response(response)
        day = data.get("day")

        assert day.get("__typename") == "DayType"
        assert "teamMembersOff" in day
        assert "noteSet" in day
        assert "tripdetailSet" in day

    def test_create_trip_detail(self):
        """Create trip detail mutation"""
        response = self.query(
            """
            mutation CreateDiveTripDetail(
                $diveSite1: String
                $diveSite2: String
                $diveGuides: [ID]
                $date: Date
                $time: String
                $tripType: String
            ) {
                createTripDetail(
                diveSite1: $diveSite1
                diveSite2: $diveSite2
                diveGuides: $diveGuides
                date: $date
                time: $time
                tripType: $tripType
                ) {
                    tripDetail {
                        id
                        diveSite1
                        diveSite2
                        diveGuides {
                            id
                        }
                        day {
                            date
                        }
                        tripType
                    }
                }
            }
             """,
            op_name="CreateDiveTripDetail",
            variables={
                "diveSite1": "Inchcape 1",
                "diveSite2": "3 Rocks",
                "diveGuides": [1],
                "date": "2021-03-30",
                "tripType": "PM_BOAT",
            },
        )
        self.assertResponseNoErrors(response)

        data = parse_response(response)
        trip_detail = data.get("createTripDetail").get("tripDetail")
        assert trip_detail["diveSite1"] == "Inchcape 1"
        assert trip_detail["diveSite2"] == "3 Rocks"
        dive_guides = trip_detail["diveGuides"]
        assert len(dive_guides) >= 0
        assert trip_detail["tripType"] == "PM_BOAT"

    def test_edit_trip_detail(self):
        """Edit trip detail mutation"""
        response = self.query(
            """
            mutation EditTripDetail(
                $id: ID,
                $diveSite1: String
                $diveSite2: String
                $diveGuides: [ID]
            ) {
                editTripDetail(
                id: $id
                diveSite1: $diveSite1
                diveSite2: $diveSite2
                diveGuides: $diveGuides
                ) {
                    tripDetail {
                        id
                        diveSite1
                        diveSite2
                        diveGuides {
                            id
                        }
                    }
                }
            }
             """,
            op_name="EditTripDetail",
            variables={
                "id": 1,
                "diveSite1": "Dibba Rock",
                "diveSite2": "3 Rocks",
                "diveGuides": [2],
            },
        )
        self.assertResponseNoErrors(response)

        data = parse_response(response)
        trip_detail = data.get("editTripDetail").get("tripDetail")

        assert trip_detail["diveSite1"] == "Dibba Rock"
        assert trip_detail["diveSite2"] == "3 Rocks"
