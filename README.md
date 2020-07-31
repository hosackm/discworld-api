# Discworld API

Discworld API is a RESTful API that contains information about the books and subseries of the [Discworld universe](https://en.wikipedia.org/wiki/Discworld).  It can be used to retrieve information about the 41 books written by Terry Pratchett. A live demo can be found [here](https://floating-ridge-73134.herokuapp.com/info).  Read on to learn about the API endpoints and to make use of this live demo.

## API

### Authorization

Authorization is required for any endpoint that modifies data in the API.  This authorization can be granted through a JWT retrieved from the apps Auth0 integration.

To receive a JWT visit the following endpoint in your webbrowser:

[https://floating-ridge-73134.herokuapp.com/login](https://floating-ridge-73134.herokuapp.com/login)

You will be redirected to a login page hosted by Auth0.  Use this page to login or create an account.  You will automatically be redirected to a page that displays your access token in a

```javascript
{
    "access_token": <ACCESS-TOKEN>
    ...
}
```

You can use this header to access endpoints that modify data.  Access to modify data will be granted after [emailing me](mailto:discworld@matthosack.com).

### Endpoints

#### Books
The endpoint `/api/books` is used to retrieve information about a specific book in the series.

```javascript
{
    "id": Integer representing the index in the database,
    "title": String of the title of the book,
    "book_number": Integer representing the number of the book in the Discworld series,
    "pages": Integer number of pages in the book,
    "year": Integer year of the first publication,
    "isbn": Integer representing the ISBN of the book,
    "subseries_number": Integer number of the book within its subseries,
    "subseries_id": Integer number representing the subseries this book belongs to,
    "image_url": String URL to the image,
    "score": Float rating for the book betwen 0 and 5
}
```

##### GET
The GET method is used to retrieve infomration about the Discworld books.  You can retrieve information about every book by sending a GET request to the `/api/books` endpoint.  You can retrieve  information about a specific book by using the `/api/books/{id}` where `{id}` is the id of the book in the database.

##### POST
POST can be used to insert books into the database.  This endpoint requires an access token with `post:books` permissions.  You must provide all information for the book to be inserted into the database.

Here's an example using curl:

```bash
curl https://floating-ridge-73134.herokuapp.com/api/books   \
    -X POST                                                 \
    -H "Content-Type: application/json"                     \
    -H "Authorization: Bearer <ACCESS_TOKEN>"               \
    -d "{                                                   \
    "title": "A Book Title",                                \
    "book_number": 1,                                       \
    "pages": 123,                                           \
    "year": 1999,                                           \
    "isbn": 1234567890,                               \
    "subseries_number": 1                                   \
    "image_url": "https://via.placeholder.com/400.png",     \
    "score": 4.8}"
```

This will return a JSON object containing the fields of the newly inserted book.

##### PATCH
A book can be modified using the PATCH HTTP method on the /api/books/{id}` endpoint.  In this case the `id` is the id of the item in the database.  This point requires a token with the `patch:books` permission.  Only the field being updated is required in the HTTP body as a JSON object.

Here is an example:

```bash
curl https://floating-ridge-73134.herokuapp.com/api/books/1 \
    -X PATCH                                                \
    -H "Authorization: Bearer <ACCESS_TOKEN>"               \
    -H "Content-Type: application/json"                     \
    -d "{                                                   \
    "title": "A Modified Title",                            \
    "score": 5.0                                            \
    }"
```

This will return a JSON object with the fields of the modified book.

##### DELETE
A book can be deleted from the database using the DELETE HTTP method on the /api/books/{id}` endpoint.  In this case the `id` is the id of the item in the database.  This point requires a token with the `delete:books` permission.

For example:

```bash
curl -X DELETE https://floating-ridge-73134.herokuapp.com/api/books/1
```

This will return a JSON object with the key `deleted_id` set to the id of the book that was deleted.

#### /api/subseries

The endpoint `/api/subseries` is used to retrieve information about a subseries in the Discworld series.

A subseries is modeled as the following:

```javascript
{
    "id": Integer key in database,
    "title": String representing the subseries title,
    "num_books": Integer number of books in the subseries
}
```

##### GET

The GET method is used to retrieve infomration about the subseries.  You can retrieve information about every subseries by sending a GET request to the `/api/subseries` endpoint.  You can retrieve specific information about a single subseries by using the `/api/subseries/{id}` where `{id}` is the id of the subseries in the database.

##### POST
POST can be used to insert subseries into the database at the endpoint `/api/subseries`.  This endpoint requires an access token with `post:subseries` permissions.  You must provide all information for the book to be inserted into the database.

Here's an example using curl:

```bash
curl https://floating-ridge-73134.herokuapp.com/api/subseries   \
    -X POST                                                     \
    -H "Content-Type: application/json"                         \
    -H "Authorization: Bearer <ACCESS_TOKEN>"                   \
    -d "{                                                       \
    "title": "Harry Potter",                                    \
    "num_books": 7                                              \
    }
```

This will return a JSON object containing the fields of the newly inserted subseries.

##### PATCH
A subseries can be modified using the PATCH HTTP method on the /api/subseries/{id}` endpoint.  In this case the `id` is the id of the item in the database.  This point requires a token with the `patch:subseries` permission.  Only the field being updated is required in the HTTP body as a JSON object.

Here is an example:

```bash
curl https://floating-ridge-73134.herokuapp.com/api/subseries/1 \
    -X PATCH                                                    \
    -H "Authorization: Bearer <ACCESS_TOKEN>"                   \
    -H "Content-Type: application/json"                         \
    -d "{                                                       \
    "title": "A New Title",                                     \
    "num_nooks": 42                                             \
    }"
```

This will return a JSON object with the fields of the modified book.

##### DELETE
A book can be deleted from the database using the DELETE HTTP method on the /api/books/{id}` endpoint.  In this case the `id` is the id of the item in the database.  This point requires a token with the `delete:books` permission.

For example:

```bash
curl -X DELETE https://floating-ridge-73134.herokuapp.com/api/subseries/1
```

This will return a JSON object with the key `deleted_id` set to the id of the book that was deleted.

### Errors

In the event that you make in invalid request or cause an internal server error, the API will return one of the following error JSON objects.

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

#### Rate Limiting

Rate limiting is set to a default of 200 requests per day and  50 request per hour.  If this limit is exceeded, request will be answered with a HTTP status code of 429.
