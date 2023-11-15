from api.queries import get_reservation_resolver
from api.models import Reservation

from . import mock_db_session, patch_db_session


class DescribeGraphqlResolvers:
    def should_return_reservation_resolver(self, mock_db_session, patch_db_session):
        # Create a mock reservation
        mock_reservation = Reservation(
            id=1,
            room_id="room_1",
            checkin_date="2023-01-01",
            checkout_date="2023-01-03",
        )

        mock_db_session.query.return_value.filter_by.return_value.first.return_value = (
            mock_reservation
        )
        mock_execution_context = {"context_key": "context_value"}

        # Call the resolver function with the mock arguments
        result = get_reservation_resolver(None, mock_execution_context, "room_1")

        assert "reservation" in result
        assert result["reservation"] == {
            "id": 1,
            "room_id": "room_1",
            "checkin_date": "2023-01-01",
            "checkout_date": "2023-01-03",
            "total_charge": None,
        }

        mock_db_session.query.assert_called_once_with(Reservation)
        mock_db_session.query.return_value.filter_by.assert_called_once_with(
            room_id="room_1"
        )
        mock_db_session.query.return_value.filter_by.return_value.first.assert_called_once()
