from flask import abort, jsonify
from flask_restful import Resource, reqparse
from ..models import Book, db
from ..caching import cache
from ..auth import requires_auth


book_post_parser = reqparse.RequestParser()
book_post_parser.add_argument("title", type=str, help="Title of book", required=True)
book_post_parser.add_argument("pages", type=int, help="Number of pages", required=True)
book_post_parser.add_argument("year", type=int, help="Year published", required=True)
book_post_parser.add_argument("isbn", type=int, help="ISBN of book", required=True)
book_post_parser.add_argument("book_number", type=int, help="Number of book in Discworld series", required=True)
book_post_parser.add_argument("image_url", type=str, help="URL to book image", required=True)
book_post_parser.add_argument("score", type=float, help="Reader rating", required=True)
book_post_parser.add_argument("subseries_id", type=int, help="Which subseries book belongs to", required=True)
book_post_parser.add_argument("subseries_number", type=int, help="Which book in the subseries", required=True)

book_patch_parser = book_post_parser.copy()
for args in book_patch_parser.args:
    args.required = False


class BooksView(Resource):
    @cache.cached(timeout=50)
    def get(self):
        books = Book.query.order_by(Book.id).all()
        return jsonify({
            "num_results": len(books),
            "books": [b.format() for b in books]
        })

    @requires_auth("post:books")
    def post(self):
        args = book_post_parser.parse_args()
        book = Book(**args)

        try:
            book.insert()
        except Exception:
            db.session.rollback()
            abort(400)

        return jsonify({"book": book.format()})


class BookView(Resource):
    @cache.cached(timeout=50)
    def get(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            abort(404)

        return jsonify({
            "book": book.format()
        })

    @requires_auth("delete:books")
    def delete(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            abort(404)

        book.delete()

        return jsonify({
            "deleted_id": book_id
        })

    @requires_auth("patch:books")
    def patch(self, book_id):
        args = book_patch_parser.parse_args()
        book = Book.query.get(book_id)
        if not book:
            abort(404)

        keys = [a.name for a in book_patch_parser.args]
        for key in keys:
            if key in args and args[key] is not None:
                setattr(book, key, args[key])

        book.update()
        return jsonify({
            "book": book.format()
        })
