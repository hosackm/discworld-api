import os
import requests
import re
import json
from xml.etree import ElementTree as ET
from collections import OrderedDict
from io import StringIO


known_titles = [
    "The Color of Magic",
    "The Light Fantastic",
    "Equal Rites",
    "Mort",
    "Sourcery",
    "Wyrd Sisters",
    "Pyramids",
    "Guards! Guards!",
    "Eric",
    "Moving Pictures",
    "Reaper Man",
    "Witches Abroad",
    "Small Gods",
    "Lords and Ladies",
    "Men at Arms",
    "Soul Music",
    "Interesting Times",
    "Maskerade",
    "Feet of Clay",
    "Hogfather",
    "Jingo",
    "The Last Continent",
    "Carpe Jugulum",
    "The Fifth Elephant",
    "The Truth",
    "Thief of Time",
    "The Last Hero",
    "The Amazing Maurice and His Educated Rodents",
    "Night Watch",
    "The Wee Free Men",
    "Monstrous Regiment",
    "A Hat Full of Sky",
    "Going Postal",
    "Thud!",
    "Wintersmith",
    "Making Money",
    "Unseen Academicals",
    "I Shall Wear Midnight",
    "Snuff",
    "Raising Steam",
    "The Shepherd's Crown"
]

def main():
    filename = "results.xml"
    root = ET.parse(filename).getroot()

    books = []

    # iterate over every result
    for book in root.findall("work"):
        # gather the fields we care about
        title = book.find("best_book//title").text
        series = ""
        if "(" in title:
            title, series = title.split("(")
            title = title.strip()
            series = series.strip(")")

        if title not in known_titles:
            print("Couldn't match title:", title)
            continue
        else:
            known_titles.remove(title)

        book_id = int(book.find("best_book//id").text)
        discworld_series = int(re.search(r"Discworld,? #(\d+)", series).groups()[0])
        subseries = re.search(r"(Witches|Rincewind|City Watch|Moist [vV]on Lipwig|Tiffany Aching|Death|Industrial Revolution)+,? #(\d+)", series)
        if subseries is None:
            subseries_num = -1
            subseries = -1
        else:
            subseries, subseries_num = subseries.groups()
            subseries_num = int(subseries_num)

        # these fields require more info
        # isbn
        # pages
        print("Getting extra information for:", title)
        url = f"https://www.goodreads.com/book/show/{book_id}.xml?key={os.getenv('GOODREADS_API_KEY')}"
        with requests.get(url) as resp:
            root = ET.parse(StringIO(resp.text)).getroot()

        isbn = root.find("book//isbn").text
        num_pages = root.find("book//num_pages").text
        if num_pages:
            num_pages = int(num_pages)
        else:
            num_pages = -1

        data = OrderedDict(
            id=book_id,
            goodreads_url=f"https://www.goodreads.com/book/show/{book_id}.xml",
            discworld_series=discworld_series,
            subseries=subseries,
            subseries_num=subseries_num,
            title=title,
            series=series,
            year=int(book.find("original_publication_year").text),
            image_url=book.find("best_book//image_url").text,
            rating=book.find("average_rating").text,
            num_pages=num_pages,
            isbn=isbn
        )

        books.append(data)

    if known_titles:
        print("Unmatched titles:", known_titles)

    # write out to json
    with open("books.json", "w") as f:
        f.write(json.dumps(books, indent=4))


if __name__ == "__main__":
    main()
