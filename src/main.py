from flask import Response, jsonify, make_response

import api.utils as utils

from routes import create_app
from routes.handlers.about import about_blueprint
from routes.handlers.api import api_blueprint
from routes.handlers.playground import playground_blueprint

app = create_app(about_blueprint, api_blueprint, playground_blueprint)


@app.errorhandler(404)
def resource_not_found(e) -> Response:
    return make_response(jsonify(error="Not found!"), 404)


def main() -> None:
    if utils.is_debug():
        utils.setup_file_logger()

    app.run(host="0.0.0.0", debug=utils.is_debug(), port=utils.api_port())

    if utils.is_debug():
        utils.logger_exit_message()


if __name__ == "__main__":
    main()
