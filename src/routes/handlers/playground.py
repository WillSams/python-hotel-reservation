from flask import Blueprint, Response, make_response
from ariadne.explorer import ExplorerGraphiQL

import api.utils as utils

playground_blueprint = Blueprint("playground", __name__)

explorer_html = ExplorerGraphiQL().html(None)


@playground_blueprint.route(
    f"/{utils.runtime_environment()}/playground", methods=["GET"]
)
def playground_handler() -> Response:
    return make_response(explorer_html, 200)
