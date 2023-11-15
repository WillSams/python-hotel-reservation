import pytest
import json

from . import flask_app

from routes.handlers.about import about_blueprint


class DescribeAboutRoutes:
    @pytest.fixture(scope="module")
    def client(self):
        app = flask_app(about_blueprint)
        with app.test_client() as client:
            yield client

    def should_return_about_page(self, client):
        response = client.get("/test/about")
        assert response.status_code == 200
        assert response.content_type == "application/json"
        data = json.loads(response.data.decode("utf-8"))
        expected_data = "Hotel Reservation API"
        assert data["name"] == expected_data
