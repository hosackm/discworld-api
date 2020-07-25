import os
import requests
from urllib.parse import quote_plus


class GoodReadsSearch:
    URL = "https://www.goodreads.com/search.xml"

    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, query, page=1):
        url = self.URL + f"?key={self.api_key}&page={page}&q=" + quote_plus(query)
        with requests.get(url) as resp:
            return resp.text


def main():
    API_KEY = os.getenv("GOODREADS_API_KEY")
    g = GoodReadsSearch(API_KEY)
    with open("page2.xml", "w") as f:
        f.write(g.search("Discworld", page=2))


if __name__ == "__main__":
    main()
