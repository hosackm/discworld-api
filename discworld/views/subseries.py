from flask import jsonify, abort
from flask_restful import Resource, fields, reqparse
from collections import OrderedDict
from ..models import Subseries, Book
from ..caching import cache


subseries_fields = OrderedDict(
    id=fields.Integer,
    title=fields.String,
    num_books=fields.Integer
)

# POSTing requires all fields
subs_post_parser = reqparse.RequestParser()
subs_post_parser.add_argument("title", type=str, help="The title of the subseries", required=True)
subs_post_parser.add_argument("num_books", type=int, help="Number of books in the subseries", required=True)

# PATCH fields are optional
subs_patch_parser = subs_post_parser.copy()
for arg in subs_patch_parser.args:
    arg.required = False


class SubseriesListView(Resource):
    @cache.cached(timeout=50)
    def get(self):
        subs = Subseries.query.order_by(Subseries.id).all()
        return jsonify({
            "num_results": len(subs),
            "subseries": [s.format() for s in subs]
        })

    def post(self):
        # insert the subseries into the database
        args = subs_post_parser.parse_args(strict=True)
        print(args)

        sub = Subseries(title=args.title, num_books=args.num_books)
        sub.insert()

        return jsonify({
            "subseries": sub.format()
        })


class SubseriesView(Resource):
    @cache.cached(timeout=50)
    def get(self, subseries_id):
        sub = Subseries.query.get(subseries_id)
        if not sub:
            abort(404)

        sub_json = {"subseries": sub.format()}

        books = Book.query.filter(Book.subseries_id == subseries_id).order_by(Book.subseries_number)
        sub_json["books"] = [b.format() for b in books]

        return jsonify(sub_json)

    def delete(self, subseries_id):
        sub = Subseries.query.get(subseries_id)
        if not sub:
            abort(404)

        sub.delete()

        return jsonify({
            "deleted_id": subseries_id
        })

    def patch(self, subseries_id):
        args = subs_patch_parser.parse_args(strict=True)
        sub = Subseries.query.get(subseries_id)

        if not sub:
            abort(404)

        # filter out unsupported args in request body
        if "title" in args and args.title is not None:
            sub.title = args.title
        if "num_books" in args and args.num_books is not None:
            sub.num_books = args.num_books

        sub.update()

        return jsonify({"subseries": sub.format()})
