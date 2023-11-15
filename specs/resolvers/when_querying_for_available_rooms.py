import pytest

from unittest.mock import MagicMock

from api.queries import get_available_rooms_resolver
from api.models import Room

from . import mock_db_session, patch_db_session


class DescribeGraphqlResolvers:
    @pytest.fixture
    def mock_is_room_available(self, mocker):
        return mocker.patch("api.queries.is_room_available")

    @pytest.fixture
    def mock_room(self, mocker):
        return mocker.MagicMock(spec=Room)

    def should_return_available_rooms_resolver(
        self, mock_db_session, patch_db_session, mock_is_room_available, mock_room
    ):
        mock_room.id = "room_1"
        mock_room.num_beds = 2
        mock_room.allow_smoking = True
        mock_room.daily_rate = 100
        mock_room.cleaning_fee = 20
        mock_save = MagicMock()
        mock_room.save = mock_save
        mock_db_session.query.return_value.filter.return_value.all.return_value = [
            mock_room
        ]
        mock_is_room_available.return_value = True
        mock_execution_context = {"context_key": "context_value"}

        # Call the resolver function with the mock arguments
        result = get_available_rooms_resolver(
            None,
            mock_execution_context,
            {"checkin_date": "2023-01-01", "checkout_date": "2023-01-03"},
        )

        assert "rooms" in result
        assert len(result["rooms"]) == 1

        # Access the first element of the list
        room_instance = result["rooms"][0]

        # Assert that the room instance is of type Room
        assert isinstance(room_instance, Room)

        # Adjust the assertions based on your actual room attributes
        assert room_instance.id == "room_1"
        assert room_instance.num_beds == 2
        assert room_instance.allow_smoking == True
        assert room_instance.daily_rate == 100
        assert room_instance.cleaning_fee == 20
