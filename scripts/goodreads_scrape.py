import os
import requests
from urllib.parse import quote_plus
from xml.etree.ElementTree import Element, parse, tostring
from io import StringIO


class GoodReadsSearch:
    URL = "https://www.goodreads.com/search.xml"

    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, query):
        page = 1
        results = Element("results")
        results_count = 0
        while results_count < 100:
            url = self.URL + f"?key={self.api_key}&page={page}&q=" + quote_plus(query)
            with requests.get(url) as resp:
                root = parse(StringIO(resp.text))

            works = root.find("search").find("results").findall("work")
            print(f"Got another {len(works)} works")
            results.extend(works)

            start = int(root.find("search").find("results-start").text)
            end = int(root.find("search").find("results-end").text)
            results_count += end + 1 - start
            page += 1

        return results


def main():
    API_KEY = os.getenv("GOODREADS_API_KEY")
    g = GoodReadsSearch(API_KEY)
    results = g.search("Discworld")
    with open("results.xml", "w") as f:
        f.write(tostring(results).decode("utf8"))


if __name__ == "__main__":
    main()
