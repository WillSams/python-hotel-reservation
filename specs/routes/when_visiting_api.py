import pytest
import json

from . import flask_app
from routes.handlers.api import api_blueprint


class DescribeAPIRoutes:
    @pytest.fixture(scope="module")
    def client(self):
        app = flask_app(api_blueprint)
        with app.test_client() as client:
            yield client

    def get_response(self, client, payload):
        response = client.post("/test/api", json=payload)

        assert response.status_code == 200
        assert response.content_type == "application/json"

        return json.loads(response.data.decode("utf-8"))

    def should_return_data_for_get_all_reservations(self, client):
        query_string = "query { getAllReservations {reservations{room_id}}}"
        query = {"query": query_string}
        response = self.get_response(client, query)
        assert "data" in response
        assert "getAllReservations" in response["data"]
        assert "reservations" in response["data"]["getAllReservations"]

    def should_return_data_for_create_reservation(self, client):
        mutation = {
            "query": (
                "mutation { createReservation( input: { "
                'room_id: "91754a14-4885-4200-a052-e4042431ffb8", '
                'checkin_date: "2023-12-31", '
                'checkout_date: "2024-01-02", '
                "total_charge: 111 }) { "
                "success errors reservation { "
                "id room_id checkin_date checkout_date total_charge } } }"
            )
        }

        response = self.get_response(client, mutation)
        assert "data" in response
        assert "createReservation" in response["data"]
        assert "reservation" in response["data"]["createReservation"]

    def should_return_data_for_get_available_rooms(self, client):
        query = {
            "query": (
                "query { getAvailableRooms( input: { "
                'checkin_date: "2023-12-31", '
                'checkout_date: "2024-01-02" }) { '
                "success errors rooms { "
                "id num_beds allow_smoking daily_rate cleaning_fee } } }"
            )
        }
        response = self.get_response(client, query)
        assert "data" in response
        assert "getAvailableRooms" in response["data"]
        assert "rooms" in response["data"]["getAvailableRooms"]
