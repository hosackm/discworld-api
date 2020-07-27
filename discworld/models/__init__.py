from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    book_number = db.Column(db.Integer)
    pages = db.Column(db.Integer)
    year = db.Column(db.Integer)
    isbn = db.Column(db.String())
    subseries_number = db.Column(db.Integer)
    image_url = db.Column(db.String())
    score = db.Column(db.Float)

    subseries_id = db.Column(db.Integer, db.ForeignKey("subseries.id"))
    subseries = db.relationship("Subseries")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "pages": self.pages,
            "year": self.year,
            "isbn": self.isbn,
            "book_number": self.book_number,
            "subseries_number": self.subseries_number,
            "subseries_id": self.subseries_id,
            "image_url": self.image_url,
            "score": self.score
        }


class Subseries(db.Model):
    __tablename__ = "subseries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    num_books = db.Column(db.Integer)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "num_books": self.num_books
        }


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    app.config["db"] = db
