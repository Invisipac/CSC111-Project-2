import requests
from bs4 import BeautifulSoup
import pprint

test_url = "/wiki/Computer_science"
d = 2

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


def create_dataset(data: dict, depth: int) -> dict:
    if depth == 0:
        return data
    else:
        for link in data:
            data[link] = get_hyperlinks(link)
            create_dataset(data[link], depth-1)

        return data


start = {test_url: {}}
dataset = create_dataset(start, d)
pprint.pprint(dataset)
