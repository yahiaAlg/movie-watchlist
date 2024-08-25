import uuid
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from json_database_utility import JSONDatabaseUtility
from routes import pages, auth, register_error_handlers


def create_app():
    
    app = Flask(__name__)
    register_error_handlers(app)
    app.config["SECRET_KEY"] = uuid.uuid4().hex
    app.wsgi_app = ProxyFix(app.wsgi_app) 

    app.config['PREFERRED_URL_SCHEME'] = 'https' 
    app.db = JSONDatabaseUtility("movies.json")
    
    # Ensure the 'movies' table exists
    if "movies" not in app.db.list_tables():
        app.db.create_table("movies")
    # Ensure the 'movies' table exists
    if "users" not in app.db.list_tables():
        app.db.create_table('users')

    app.register_blueprint(pages)
    app.register_blueprint(auth)
    return app



if __name__=="__main__":
    create_app().run(debug=True, ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=5000)
