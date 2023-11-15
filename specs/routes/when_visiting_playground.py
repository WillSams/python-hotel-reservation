import pytest

from . import flask_app
from routes.handlers.playground import playground_blueprint


class DescribePlaygroundRoutes:
    @pytest.fixture(scope="module")
    def client(self):
        app = flask_app(playground_blueprint)
        with app.test_client() as client:
            yield client

    def should_return_graphiql_page(self, client):
        response = client.get("/test/playground")
        assert response.status_code == 200
        assert response.content_type == "text/html; charset=utf-8"

        expected = b"GraphQL Contributors\n *  All rights reserved."
        assert expected in response.data
