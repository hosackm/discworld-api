def test_api_get_books_starts_empty(client):
    resp = client.get("/api/books")
    assert resp.status_code == 200
    assert resp.json["num_results"] == 0
    assert resp.json["books"] == []


def test_api_get_subseries_starts_empty(client):
    resp = client.get("/api/subseries")
    assert resp.status_code == 200
    assert resp.json["num_results"] == 0
    assert resp.json["subseries"] == []


def test_api_post_book_throws_exception_without_associated_subseries(client):
    title = "The Hounds of Baskervilles"
    book_number = 5
    pages = 256
    year = 1902
    isbn = "1514698935"
    subseries_number = 1
    image_url = "https://via.placeholder.com/150"
    score = 4.12
    # missing a subseries

    data = dict(title=title, book_number=book_number, pages=pages,
                year=year, isbn=isbn, subseries_number=subseries_number,
                image_url=image_url, score=score)

    resp = client.post("/api/books", data=data)
    assert resp.status_code == 400
    assert "subseries_id" in resp.json["message"]


def test_api_post_subseries_persists_subseries(client):
    # add a single subseries to the db
    title = "The Hardy Boys"
    nbooks = 58
    subseries = dict(title=title, num_books=nbooks)
    resp = client.post("/api/subseries", data=subseries)
    assert resp.status_code == 200

    # make sure it persists
    resp = client.get("/api/subseries")
    assert resp.status_code == 200
    assert resp.json["num_results"] == 1
    assert resp.json["subseries"][0]["title"] == title
    assert resp.json["subseries"][0]["num_books"] == nbooks


def test_api_post_book_persists_in_database(client):
    # POST a subseries
    title = "The Hardy Boys"
    nbooks = 58
    subseries = dict(title=title, num_books=nbooks)
    resp = client.post("/api/subseries", data=subseries)
    assert resp.status_code == 200

    title = "The Hounds of Baskervilles"
    book_number = 5
    pages = 256
    year = 1902
    isbn = "1514698935"
    subseries_number = 1
    image_url = "https://via.placeholder.com/150"
    score = 4.12
    subseries_id = 1

    # POST a book to database
    data = dict(title=title, book_number=book_number, pages=pages,
                year=year, isbn=isbn, subseries_number=subseries_number,
                image_url=image_url, score=score, subseries_id=subseries_id)
    resp = client.post("/api/books", data=data)
    assert resp.status_code == 200

    # Make sure book exists in book collection endpoint
    resp = client.get("/api/books")
    assert resp.status_code == 200
    assert resp.json["num_results"] == 1
    assert resp.json["books"][0]["title"] == title
    assert resp.json["books"][0]["book_number"] == book_number
    assert resp.json["books"][0]["pages"] == pages
    assert resp.json["books"][0]["year"] == year
    assert resp.json["books"][0]["isbn"] == isbn
    assert resp.json["books"][0]["subseries_number"] == subseries_number
    assert resp.json["books"][0]["image_url"] == image_url
    assert resp.json["books"][0]["score"] == score
    assert resp.json["books"][0]["subseries_id"] == subseries_id

    book_id = resp.json["books"][0]["id"]

    # Make sure book exists in /api/books/{id} endpoint
    resp = client.get(f"/api/books/{book_id}")
    assert resp.status_code == 200
    assert resp.json["book"]["title"] == title
    assert resp.json["book"]["book_number"] == book_number
    assert resp.json["book"]["pages"] == pages
    assert resp.json["book"]["year"] == year
    assert resp.json["book"]["isbn"] == isbn
    assert resp.json["book"]["subseries_number"] == subseries_number
    assert resp.json["book"]["image_url"] == image_url
    assert resp.json["book"]["score"] == score
    assert resp.json["book"]["subseries_id"] == subseries_id


def test_patch_subseries_persists(client):
    # POST a subseries
    title = "The Hardy Boys"
    nbooks = 58
    subseries = dict(title=title, num_books=nbooks)
    resp = client.post("/api/subseries", data=subseries)
    assert resp.status_code == 200

    # PATCH the subseries title
    new_title = "Nancy Drew"
    resp = client.patch("/api/subseries/1", data={"title": new_title})
    assert resp.status_code == 200
    assert resp.json["subseries"]["title"] == new_title

    resp = client.get("/api/subseries/1")
    assert resp.status_code == 200
    assert resp.json["subseries"]["title"] == new_title

    # PATCH the subseries num_books
    new_length = 56
    resp = client.patch("/api/subseries/1", data={"num_books": new_length})
    assert resp.status_code == 200
    assert resp.json["subseries"]["num_books"] == new_length

    resp = client.get("/api/subseries/1")
    assert resp.status_code == 200
    resp.json["subseries"]["title"] == new_length


def test_patch_book_persists(client):
    # POST a subseries
    subseries = dict(title="The Hardy Boys", num_books=58)
    client.post("/api/subseries", data=subseries)

    data = dict(
        title="The Hounds of Baskervilles",
        book_number=5,
        pages=256,
        year=1902,
        isbn="1514698935",
        subseries_number=1,
        image_url="https://via.placeholder.com/150",
        score=4.12,
        subseries_id=1)

    # POST a book to database
    client.post("/api/books", data=data)

    # PATCH each element of the book
    resp = client.patch("/api/books/1", data={"title": "New Title"})
    assert resp.status_code == 200
    assert resp.json["book"]["title"] == "New Title"
    resp = client.patch("/api/books/1", data={"book_number": 2})
    assert resp.status_code == 200
    assert resp.json["book"]["book_number"] == 2
    resp = client.patch("/api/books/1", data={"pages": 123})
    assert resp.status_code == 200
    assert resp.json["book"]["pages"] == 123
    resp = client.patch("/api/books/1", data={"year": 2020})
    assert resp.status_code == 200
    assert resp.json["book"]["year"] == 2020
    resp = client.patch("/api/books/1", data={"isbn": "1234567890"})
    assert resp.status_code == 200
    assert resp.json["book"]["isbn"] == "1234567890"
    resp = client.patch("/api/books/1", data={"subseries_number": 9})
    assert resp.status_code == 200
    assert resp.json["book"]["subseries_number"] == 9
    resp = client.patch("/api/books/1", data={"image_url": "http://placeholder.com/new-image-url.jpg"})
    assert resp.status_code == 200
    assert resp.json["book"]["image_url"] == "http://placeholder.com/new-image-url.jpg"
    resp = client.patch("/api/books/1", data={"score": 3.14})
    assert resp.status_code == 200
    assert resp.json["book"]["score"] == 3.14


def test_delete_subseries_persists(client):
    # add a single subseries to the db
    title = "The Hardy Boys"
    nbooks = 58
    subseries = dict(title=title, num_books=nbooks)
    client.post("/api/subseries", data=subseries)

    resp = client.delete("/api/subseries/1")
    assert resp.status_code

    resp = client.get("/api/subseries")
    assert resp.json["num_results"] == 0


def test_delete_book_persists(client):
    # POST a subseries
    subseries = dict(title="The Hardy Boys", num_books=58)
    client.post("/api/subseries", data=subseries)

    data = dict(
        title="The Hounds of Baskervilles",
        book_number=5,
        pages=256,
        year=1902,
        isbn="1514698935",
        subseries_number=1,
        image_url="https://via.placeholder.com/150",
        score=4.12,
        subseries_id=1)

    # POST a book to database
    client.post("/api/books", data=data)

    # DELETE the book
    resp = client.delete("/api/books/1")
    assert resp.status_code == 200
    assert resp.json["deleted_id"] == 1

    resp = client.get("/api/books")
    assert resp.status_code == 200
    assert resp.json["num_results"] == 0


def test_post_multiple_subseries_persist_correctlty(client):
    subseries = (
        {"title": "The Hardy Boys", "num_books": 58},
        {"title": "Nancy Drew", "num_books": 56},
        {"title": "Twilight", "num_books": 4},
        {"title": "Harry Potter", "num_books": 7},
        {"title": "Hunger Games", "num_books": 3}
    )

    for sub in subseries:
        resp = client.post("/api/subseries", data=sub)
        assert resp.status_code == 200

    resp = client.get("/api/subseries")
    assert resp.status_code == 200

    # Make sure the subseries info matches...


# def test_post_multiple_books_persist_correctlty(client):
#     assert "POST multiple times" == ""


def test_non_existent_endpoints_return_404s(client):
    non_existent = [
        (client.get, "/api/books/9999"),
        (client.delete, "/api/books/9999"),
        (client.patch, "/api/books/9999"),

        (client.get, "/api/subseries/123456"),
        (client.delete, "/api/subseries/123456"),
        (client.patch, "/api/subseries/123456")
    ]

    for func, endpoint in non_existent:
        resp = func(endpoint)
        assert resp.status_code == 404
        assert "not found" in resp.json["message"]


def test_incorrect_methods_return_405s(client):
    bad_methods = [
        (client.put, "/api/books"),
        (client.put, "/api/subseries"),
        # ... add more if you think of them
    ]

    for func, endpoint in bad_methods:
        resp = func(endpoint)
        assert resp.status_code == 405
        assert "method is not allowed" in resp.json["message"]
