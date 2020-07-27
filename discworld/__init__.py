import requests
from flask import Flask, jsonify, request, abort, redirect
from flask_restful import Api
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address as gra
from .models import setup_db
from .views.books import BooksView, BookView
from .views.subseries import SubseriesView, SubseriesListView
from .auth import requires_auth
from .caching import cache


def create_app(testing_config=None):
    # create base Flask app and configure based on environment
    app = Flask(__name__)
    if not testing_config:
        app.config.from_pyfile("settings.py")
    else:
        app.config.from_mapping(testing_config)

    # setup db and migrations
    setup_db(app)
    Migrate(app, app.config["db"])

    # Add flask-restful API resources
    api = Api(app)
    api.add_resource(BooksView, "/api/books")
    api.add_resource(BookView, "/api/books/<int:book_id>")
    api.add_resource(SubseriesListView, "/api/subseries")
    api.add_resource(SubseriesView, "/api/subseries/<int:subseries_id>")

    # add rate limiter to entire application
    Limiter(app, key_func=gra, default_limits="200/day 50/hour".split())

    # add cache
    cache.init_app(app)
    app.cache = cache

    # add non-API endpoints
    add_login_flow_routes(app)
    register_error_handlers(app)

    return app


def add_login_flow_routes(app):
    @app.route("/login")
    def login():
        url = (f"https://{app.config['AUTH0_DOMAIN']}/authorize?"
               f"audience={app.config['AUTH0_AUDIENCE']}&response_type=code&"
               f"client_id={app.config['AUTH0_CLIENT_ID']}&"
               f"redirect_uri={app.config['AUTH0_CALLBACK_URI']}")
        return redirect(url)

    @app.route("/callback")
    def logged_in():
        code = request.args.get("code")
        if not code:
            abort(400)

        url = f"https://{app.config['AUTH0_DOMAIN']}/oauth/token"
        params = {
            "grant_type": "authorization_code",
            "client_id": app.config["AUTH0_CLIENT_ID"],
            "client_secret": app.config["AUTH0_CLIENT_SECRET"],
            "code": code,
            "redirect_uri": app.config["AUTH0_CALLBACK_URI"]
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # retrieve token using code
        resp = requests.post(url, data=params, headers=headers)
        if resp.status_code != 200:
            abort(400)

        return jsonify(resp.json())

    @app.route("/admin")
    @requires_auth("post:books")
    def admin():
        return "You have valid administrator privileges"


def register_error_handlers(app):
    """
    Register error handlers.  Requests that are aborted inside the Flask Restful
    api will be handled by Flask Restful
    """

    # Server error
    @app.errorhandler(500)
    def error_500(e):
        return jsonify({
            "error": "Internal server error 500"
        })

    # Requested non-existent url endpoint
    @app.errorhandler(404)
    def error_404(e):
        return jsonify({
            "message": "Resource not found"
        })

    # Authorization non-existent or invalid
    @app.errorhandler(401)
    def error_401(e):
        return jsonify({
            "message": "You must provide valid authorization for resource"
        })

    # User not authorized for this resource
    @app.errorhandler(403)
    def error_403(e):
        return jsonify({
            "message": "You are not authorized for resource"
        })

def get_cache():
    cache = Cache(config={"CACHE-TYPE": "simple"})
    return cache
