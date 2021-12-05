import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "cooking.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from cooking import db
    db.init_app(app)
    # apply the blueprints to the app
    from cooking.routers import participant
    from cooking.routers import main
    from cooking.routers import command
    from cooking.routers import auth
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(command.bp)
    app.register_blueprint(participant.bp)

    return app
