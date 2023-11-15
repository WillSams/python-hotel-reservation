from flask import Blueprint, jsonify

import api.utils as utils

about_blueprint = Blueprint("about", __name__)
about_url = f"/{utils.runtime_environment()}/about"


@about_blueprint.route(about_url, methods=["GET"])
def about_handler():
    api_desc = """This is a GraphQL API that allows you to create and list
    reservations as well as the ability to list available rooms for a given
    date range."""
    response_body = {"name": "Hotel Reservation API", "description": api_desc}
    return jsonify(response_body), 200
