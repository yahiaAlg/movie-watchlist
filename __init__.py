import uuid
from flask import Flask

from .json_database_utility import JSONDatabaseUtility
from .routes import pages


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = uuid.uuid4().hex
    app.db = JSONDatabaseUtility("movies.json")
    # Ensure the 'movies' table exists
    if "movies" not in app.db.list_tables():
        app.db.create_table("movies")

    app.register_blueprint(pages)
    return app
