import time
from queue import Queue

import requests
from bs4 import BeautifulSoup
import pprint
import threading

test_url = "Computer_science"
d = 2

def get_hyperlinks(page_url: str, data: dict = None) -> dict:
    url_base = "https://en.wikipedia.org/wiki/"
    page = requests.get(url_base + page_url)

    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all('a')

    word_filter = {':', 'Glossary', 'History_of', 'List_of', 'Timeline_of'}

    usable_links = []
    for link in links:
        url = link.get('href')
        if (url and
                (url not in usable_links) and
                (url.count('/') == 2) and
                ('/wiki/' in url) and
                (page_url not in url) and
                (':' not in url) and
                (all(word not in url for word in word_filter))):
            usable_links.append(url[6:])

    usable_links.sort()
    if data is not None:
        data[page_url] = {link: dict() for link in usable_links}

    return {link: dict() for link in usable_links}


def create_dataset(data: dict, depth: int) -> dict:
    if depth == 0:
        return data
    elif depth == d - 1: # or depth == d - 2:
        threads = []
        for link in data:
            thread = threading.Thread(target=get_hyperlinks, args=(link, data))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        for l in data:
            create_dataset(data[l], depth - 1)
    else:
        for link in data:
            data[link] = get_hyperlinks(link)
            create_dataset(data[link], depth-1)

        return data


def create_dataset_original(data: dict, depth: int) -> dict:
    if depth == 0:
        return data
    else:
        for link in data:
            data[link] = get_hyperlinks(link)
            create_dataset_original(data[link], depth-1)

        return data


if __name__ == "__main__":
    start = {test_url: {}}

    start_time = time.time()
    dataset = create_dataset(start, d)
    end_time = time.time()
    print(end_time - start_time)

    # pprint.pprint(dataset)

    # start_time = time.time()
    # dataset = create_dataset_original(start, d)
    # end_time = time.time()
    # print(end_time - start_time)

    # pprint.pprint(dataset)
