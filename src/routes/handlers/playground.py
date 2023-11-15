from flask import Blueprint
from ariadne.explorer import ExplorerGraphiQL

import api.utils as utils

playground_blueprint = Blueprint("playground", __name__)

explorer_html = ExplorerGraphiQL().html(None)


@playground_blueprint.route(
    f"/{utils.runtime_environment()}/playground", methods=["GET"]
)
def playground_handler():
    return explorer_html, 200
