from routes import create_app


def flask_app(blueprint):
    app = create_app(blueprint)
    app.config.update({"TESTING": True})
    return app
