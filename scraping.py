import requests
from bs4 import BeautifulSoup
import pprint

test_url = "/wiki/Computer_science"


def get_hyperlinks(page_url: str) -> list[str]:
    url_base = "https://en.wikipedia.org"
    page = requests.get(url_base + page_url)

    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all('a')

    usable_links = []
    for link in links:
        url = link.get('href')
        if (url and
                (url not in usable_links) and
                (url.count('/') == 2) and
                ('/wiki/' in url) and
                (url not in page_url) and
                (':' not in url) and
                ('Glossary' not in url)):
            usable_links.append(url)

    return sorted(usable_links)


pprint.pprint(get_hyperlinks(test_url))
