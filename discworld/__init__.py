from flask import Flask, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from .models import setup_db
from .views.books import BooksView, BookView
from .views.subseries import SubseriesView, SubseriesListView


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(BooksView, "/api/books")
    api.add_resource(BookView, "/api/books/<int:book_id>")
    api.add_resource(SubseriesListView, "/api/subseries")
    api.add_resource(SubseriesView, "/api/subseries/<int:subseries_id>")

    setup_db(app)
    register_error_handlers(app)

    Migrate(app, app.config["db"])

    return app


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
