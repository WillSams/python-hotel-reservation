from flask import Blueprint, jsonify, request, Response, make_response

from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    graphql_sync,
    snake_case_fallback_resolvers,
    ObjectType,
)

import api.utils as utils
from api.queries import (
    get_reservation_resolver,
    get_all_reservations_resolver,
    get_available_rooms_resolver,
)
from api.mutations import (
    create_reservation_resolver,
)

api_blueprint = Blueprint("api", __name__)


query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("getReservation", get_reservation_resolver)
query.set_field("getAllReservations", get_all_reservations_resolver)
query.set_field("getAvailableRooms", get_available_rooms_resolver)

mutation.set_field("createReservation", create_reservation_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)


@api_blueprint.route(f"/{utils.runtime_environment()}/api", methods=["POST"])
def api_handler() -> Response:
    try:
        data = request.get_json()
    except Exception as e:
        utils.Logger.error(f"Error parsing JSON: {e}")
        return make_response(jsonify({"error": "Invalid JSON"}), 400)

    try:
        success, result = graphql_sync(
            schema=schema, data=data, context_value={"request": request}
        )
    except Exception as e:
        utils.Logger.error(f"GraphQL execution error: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

    status_code = 200 if success else 400
    utils.Logger.info(f"GraphQL response: {result}")
    return make_response(jsonify(result), status_code)
