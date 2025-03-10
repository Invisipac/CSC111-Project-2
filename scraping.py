import requests
from bs4 import BeautifulSoup
import pprint

test_url = "/wiki/Computer_science"


def get_hyperlinks(page_url: str) -> dict:
    url_base = "https://en.wikipedia.org"
    page = requests.get(url_base + page_url)

    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all('a')

    word_filter = {':', 'Glossary', 'History_of', 'List_of', 'Timeline_of', '_'}

    usable_links = []
    for link in links:
        url = link.get('href')
        if (url and
                (url not in usable_links) and
                (url.count('/') == 2) and
                ('/wiki/' in url) and
                (url not in page_url) and
                (':' not in url) and
                (all(word not in url for word in word_filter))):
            usable_links.append(url)

    usable_links.sort()
    return {link: dict() for link in usable_links}


pprint.pprint(get_hyperlinks(test_url))
