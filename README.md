# Discworld API

Discworld API is a RESTful API that contains information about the books and subseries of the [Discworld universe](https://en.wikipedia.org/wiki/Discworld).  It can be used to retrieve information about the 41 books written by Terry Pratchett. A live demo can be found [here](https://floating-ridge-73134.herokuapp.com/).  Read on to learn about the API endpoints and to make use of this live demo.

## API

### Authorization

    * /admin - administrator page that requires administrator priveleges to access
    * /login - visit in browser.  create login through Auth0 interface.  email discworld@matthosack.com to request POST/PATCH/DELETE access for books and subseries
    * /callback - Auth0 will redirect logins to this endpoint.  You will be able to receive the access token in the JSON body.

### Endpoints

#### Books

##### GET
##### POST
##### PATCH
##### DELETE


The endpoint `/api/books` is used to retrieve information about a specific book in the series.

Model {
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    book_number = db.Column(db.Integer)
    pages = db.Column(db.Integer)
    year = db.Column(db.Integer)
    isbn = db.Column(db.String())
    subseries_number = db.Column(db.Integer)
    image_url = db.Column(db.String())
    score = db.Column(db.Float)
}

#### /api/subseries

The endpoint `/api/subseries` is used to retrieve information about a subseries in the Discworld series.

Model {
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    num_books = db.Column(db.Integer)
}


##### GET
##### POST
##### PATCH
##### DELETE

### Errors

```python
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
```