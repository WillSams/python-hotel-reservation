def create_app(*blueprints):
    from flask import Flask

    app = Flask(__name__)
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app


#
