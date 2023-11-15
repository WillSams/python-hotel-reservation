import pytest

from sqlalchemy.orm import Session


@pytest.fixture
def mock_db_session(mocker):
    yield mocker.MagicMock(spec=Session)


@pytest.fixture
def patch_db_session(mocker, mock_db_session):
    yield mocker.patch("api.queries.DbSession", return_value=mock_db_session)
